"""Prepare a measured voice/music mix, corrected captions and SRT. Never synthesizes speech.

uv run --with numpy --with imageio-ffmpeg python scripts/prepare-narration.py narration-input.json public/narration
Input: {voice, music?, musicGainDb?: -24, duckDb?: -12, captions: [{startMs,endMs,text}]}
Paths are relative to the input JSON. Times refer to the actual voice file, including pauses.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import wave

import numpy as np

# Reuse the skill's existing decoder without changing its music-editing workflow.
spec = importlib.util.spec_from_file_location('film_audio', Path(__file__).with_name('audio-edit.py'))
audio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio)


def validate_captions(captions, duration_ms):
    if not isinstance(captions, list) or not captions:
        raise ValueError('Provide corrected, timed captions for the actual voice track')
    previous = 0
    for c in captions:
        start, end, text = c.get('startMs'), c.get('endMs'), c.get('text')
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in (start, end)):
            raise ValueError('Caption times must be finite milliseconds')
        if not (previous <= start < end <= duration_ms):
            raise ValueError('Captions must be ordered, non-overlapping and inside the voice duration')
        if not isinstance(text, str) or not text.strip() or '-->' in text or '\n\n' in text or '\r' in text:
            raise ValueError('Caption text must be nonempty plain text without SRT separators')
        previous = end


def stamp(milliseconds):
    ms = round(milliseconds)
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02},{ms:03}'


def mix(voice, music, gain_db=-24, duck_db=-12):
    if not len(voice) or np.max(np.abs(voice)) < 0.001:
        raise ValueError('Voice track is empty or silent')
    if not (-60 <= gain_db <= 0 and -40 <= duck_db <= 0):
        raise ValueError('Use musicGainDb in [-60,0] and duckDb in [-40,0]')
    # 10 ms energy windows, 80 ms attack and 200 ms release measured from speech.
    hop = audio.SR // 100
    count = math.ceil(len(voice) / hop)
    padded = np.pad(voice, ((0, count * hop - len(voice)), (0, 0)))
    rms = np.sqrt(np.mean(padded.reshape(count, hop, 2) ** 2, axis=(1, 2)))
    speech = rms > max(0.004, float(np.max(rms)) * 0.04)
    envelope = np.ones(count)
    duck = 10 ** (duck_db / 20)
    for i in np.flatnonzero(speech):
        left, right = max(0, i - 8), min(count, i + 21)
        envelope[left:i + 1] = np.minimum(envelope[left:i + 1], np.linspace(1, duck, i - left + 1))
        envelope[i:right] = np.minimum(envelope[i:right], np.linspace(duck, 1, right - i))
    gain = np.interp(np.arange(len(voice)) / hop, np.arange(count), envelope)
    result = voice.copy()
    if music is not None:
        if not len(music):
            raise ValueError('Music track is empty')
        bed = np.tile(music, (math.ceil(len(voice) / len(music)), 1))[:len(voice)].copy()
        fade = min(audio.SR, len(bed) // 2)
        bed[:fade] *= np.linspace(0, 1, fade)[:, None]
        bed[-fade:] *= np.linspace(1, 0, fade)[:, None]
        result += bed * gain[:, None] * 10 ** (gain_db / 20)
    peak = float(np.max(np.abs(result)))
    # Preserve voice dynamics; attenuate only when needed to leave 1 dB peak headroom.
    attenuation = min(1, 10 ** (-1 / 20) / peak)
    return result * attenuation, {'peakBefore': peak, 'peakAfter': peak * attenuation,
        'attenuationDb': 20 * math.log10(attenuation), 'speechWindows': int(speech.sum()),
        'duckMinimumDb': 20 * math.log10(float(gain.min())), 'sampleRate': audio.SR}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    if args.out.resolve().parent.name != 'public':
        raise ValueError('Output must be a new folder directly inside public')
    config = json.loads(args.input.read_text())
    voice = audio.decode(str((args.input.parent / config['voice']).resolve()))
    duration_ms = len(voice) / audio.SR * 1000
    captions = config['captions']
    validate_captions(captions, duration_ms)
    music = audio.decode(str((args.input.parent / config['music']).resolve())) if config.get('music') else None
    result, evidence = mix(voice, music, config.get('musicGainDb', -24), config.get('duckDb', -12))
    args.out.mkdir(parents=True, exist_ok=False)
    with wave.open(str(args.out / 'audio.wav'), 'wb') as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(audio.SR)
        handle.writeframes(np.rint(result * 32767).astype('<i2').tobytes())
    manifest = {'durationMs': duration_ms, 'audio': f'{args.out.name}/audio.wav', 'captions': captions}
    (args.out / 'narration.json').write_text(json.dumps(manifest, indent=2) + '\n')
    srt = '\n\n'.join(f'{i}\n{stamp(c["startMs"])} --> {stamp(c["endMs"])}\n{c["text"]}' for i, c in enumerate(captions, 1))
    (args.out / 'captions.srt').write_text(srt + '\n')
    evidence.update({'durationMs': duration_ms, 'captionCount': len(captions), 'music': music is not None,
        'listeningReview': 'NOT_REVIEWED', 'transcriptAccuracy': 'NOT_REVIEWED'})
    (args.out / 'audio-checks.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps(evidence))


if __name__ == '__main__':
    main()
