"""Decode a quality-test manifest and compare encoded review frames with their source stills.

uv run --with numpy --with pillow --with imageio-ffmpeg python scripts/check-media.py out/proof/manifest.json
This checks technical fidelity, not product truth, pacing, legibility or listening quality.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
import numpy as np
from PIL import Image


def compare_audio(actual, reference):
    if not len(reference) or len(actual) < len(reference):
        raise ValueError('TRUNCATED_AUDIO')
    # Account for bounded AAC priming; report the measured offset instead of hiding it.
    size = 1 << (len(actual) + len(reference) - 1).bit_length()
    correlation = np.fft.irfft(np.fft.rfft(actual, size) * np.conj(np.fft.rfft(reference, size)), size)
    lags = np.arange(-min(16000, len(reference) - 1), min(16000, len(reference) - 1) + 1)
    lag = int(lags[np.argmax(correlation[lags % size])])
    if abs(lag) > 960:
        raise ValueError(f'AUDIO_SYNC: {lag / 16:.2f} ms exceeds 60 ms')
    a, b = actual[max(0, lag):], reference[max(0, -lag):]
    length = min(len(a), len(b))
    error = float(np.sqrt(np.mean((a[:length] - b[:length]) ** 2)) / max(0.001, np.sqrt(np.mean(b[:length] ** 2))))
    if error > 0.15:
        raise ValueError(f'AUDIO_CONTENT: relative error {error:.3f}')
    return {'offsetMs': lag / 16, 'relativeError': error}


def check(job, directory):
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    path = directory / job['file']
    reader = imageio_ffmpeg.read_frames(str(path))
    try:
        metadata = next(reader)
    finally:
        reader.close()
    if tuple(metadata['size']) != (job['width'], job['height']):
        raise ValueError(f'{path.name}: DIMENSIONS')
    if abs(metadata['fps'] - job['fps']) > 0.01:
        raise ValueError(f'{path.name}: FPS')
    # AAC can add two 1024-sample packets plus rounded container metadata;
    # exact video length is enforced independently by the decoded frame count.
    tolerance = max(1.5 / job['fps'], 0.06 if job['audio'] else 0)
    if abs(metadata['duration'] - job['frames'] / job['fps']) > tolerance:
        raise ValueError(f'{path.name}: DURATION')
    result = subprocess.run([ff, '-v', 'error', '-xerror', '-i', str(path), '-map', '0:v:0', '-map', '0:a?',
        '-progress', 'pipe:1', '-nostats', '-f', 'null', '-'], capture_output=True, text=True, check=True)
    counts = re.findall(r'^frame=(\d+)$', result.stdout, re.M)
    if not counts or int(counts[-1]) != job['frames']:
        raise ValueError(f'{path.name}: FRAME_COUNT')
    info = subprocess.run([ff, '-hide_banner', '-i', str(path)], capture_output=True, text=True).stderr
    if ('Audio:' in info) != job['audio']:
        raise ValueError(f'{path.name}: AUDIO_PRESENCE')
    audio_evidence = None
    if job['audio']:
        samples = subprocess.run([ff, '-v', 'error', '-i', str(path), '-vn', '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
        pcm = np.frombuffer(samples, dtype='<f4')
        if not len(pcm) or np.max(np.abs(pcm)) < 0.001:
            raise ValueError(f'{path.name}: SILENT_AUDIO')
        if np.max(np.abs(pcm)) > 1.0:
            raise ValueError(f'{path.name}: CLIPPED_AUDIO')
        if job.get('audioReference'):
            raw = subprocess.run([ff, '-v', 'error', '-i', str(directory / job['audioReference']), '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'], capture_output=True, check=True).stdout
            reference = np.frombuffer(raw, dtype='<f4')[:round(job['frames'] / job['fps'] * 16000)]
            audio_evidence = compare_audio(pcm, reference)
    frames = []
    for sample in job['samples']:
        output = directory / sample['decoded']
        subprocess.run([ff, '-v', 'error', '-i', str(path), '-vf', f"select=eq(n\\,{sample['frame']}),scale={job['playerWidth']}:-1", '-frames:v', '1', '-y', str(output)], check=True)
        actual = np.asarray(Image.open(output).convert('RGB'), dtype=float)
        with Image.open(directory / sample['still']) as source:
            reference = np.asarray(source.convert('RGB').resize((actual.shape[1], actual.shape[0]), Image.Resampling.BICUBIC), dtype=float)
        edges = np.max(np.abs(np.diff(reference, axis=1, prepend=reference[:, :1])), axis=2) > 30
        if not edges.any():
            raise ValueError(f'{path.name}: EMPTY_REFERENCE')
        error = float(np.abs(actual - reference)[edges].mean())
        if error > 18:
            raise ValueError(f'{path.name}: ENCODE_FIDELITY at frame {sample["frame"]}: {error:.2f}')
        frames.append({'frame': sample['frame'], 'edgeMeanError': error, 'image': sample['decoded']})
    return {'file': job['file'], 'status': 'PASS', 'decodedFrames': int(counts[-1]), 'audioComparison': audio_evidence, 'samples': frames}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    if not manifest.get('renders'):
        raise ValueError('Manifest has no renders')
    results = [check(job, args.manifest.parent) for job in manifest['renders']]
    negative = {}
    for key, expected in [('fps', 'FPS'), ('frames', 'DURATION'), ('audio', 'AUDIO_PRESENCE')]:
        broken = copy.deepcopy(manifest['renders'][0])
        broken[key] = {'fps': 15, 'frames': broken['frames'] + 10, 'audio': not broken['audio']}[key]
        try:
            check(broken, args.manifest.parent)
        except ValueError as error:
            if expected not in str(error):
                raise
            negative[key] = str(error)
        else:
            raise ValueError(f'Broken {key} contract unexpectedly passed')
    broken = copy.deepcopy(manifest['renders'][0])
    original = args.manifest.parent / broken['file']
    broken['file'] = 'deliberately-blurred.mp4'
    broken['frames'] = broken['fps']
    broken['audio'] = False
    broken.pop('audioReference', None)
    broken['samples'] = [dict(broken['samples'][0], decoded='deliberately-blurred.png')]
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(original), '-t', '1',
        '-vf', 'gblur=sigma=12', '-an', '-c:v', 'libx264', '-crf', '18', '-y', str(args.manifest.parent / broken['file'])], check=True)
    try:
        check(broken, args.manifest.parent)
    except ValueError as error:
        if 'ENCODE_FIDELITY' not in str(error):
            raise
        negative['blur'] = str(error)
    else:
        raise ValueError('Deliberately blurred encode unexpectedly passed')
    pairs = manifest.get('fpsPairs', [])
    for first, second in pairs:
        a = np.asarray(Image.open(args.manifest.parent / first), dtype=float)
        b = np.asarray(Image.open(args.manifest.parent / second), dtype=float)
        if a.shape != b.shape or float(np.abs(a - b).mean()) > 1:
            raise ValueError(f'FPS_RETIMING: {first} vs {second}')
    report = {'status': 'TECHNICAL_PASS', 'renders': results, 'fpsPairs': len(pairs), 'negativeCases': negative,
        'visualReview': 'NOT_REVIEWED', 'audioListening': 'NOT_REVIEWED'}
    (args.manifest.parent / 'media-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'TECHNICAL_PASS: {len(results)} complete decodes, {len(pairs)} matching 30/60 fps review frames')


if __name__ == '__main__':
    main()
