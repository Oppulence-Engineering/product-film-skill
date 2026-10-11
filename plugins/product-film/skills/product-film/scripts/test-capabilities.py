"""Small behavioral tests for the new audio and capture helpers. Run via quality-test.ts or uv."""
from datetime import datetime, timedelta, timezone
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


voice = load('narration', 'prepare-narration.py')
capture = load('capture', 'capture-preflight.py')
media = load('media', 'check-media.py')


class NarrationTests(unittest.TestCase):
    def test_audio_comparison_measures_padding_and_rejects_shifted_content(self):
        reference = np.random.default_rng(0).normal(0, 0.1, 32000)
        measured = media.compare_audio(np.pad(reference, (683, 0)), reference)
        self.assertEqual(measured['offsetMs'], 42.6875)
        self.assertLess(measured['relativeError'], 0.001)
        with self.assertRaisesRegex(ValueError, 'AUDIO_SYNC'):
            media.compare_audio(np.pad(reference, (8000, 0)), reference)
        with self.assertRaisesRegex(ValueError, 'AUDIO_CONTENT'):
            media.compare_audio(reference * 0.5, reference)

    def test_nested_narration_output_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'public' / 'nested' / 'voice'
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('prepare-narration.py')),
                'unused.json', str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('directly inside public', result.stderr)
            self.assertFalse(output.exists())
    def test_preserves_valid_caption_text_and_millisecond_timing(self):
        captions = [{'startMs': 100, 'endMs': 1900, 'text': 'Eigenn: $1,150,000'}]
        voice.validate_captions(captions, 2000)
        self.assertEqual(voice.stamp(captions[0]['endMs']), '00:00:01,900')
        self.assertEqual(voice.stamp(3600001), '01:00:00,001')

    def test_rejects_invalid_captions(self):
        for captions in [[], [{'startMs': -1, 'endMs': 10, 'text': 'a'}],
            [{'startMs': 10, 'endMs': 10, 'text': 'a'}],
            [{'startMs': 0, 'endMs': 2001, 'text': 'a'}],
            [{'startMs': float('nan'), 'endMs': 10, 'text': 'a'}],
            [{'startMs': 0, 'endMs': 10, 'text': ' '}],
            [{'startMs': 0, 'endMs': 1000, 'text': 'a'}, {'startMs': 999, 'endMs': 1500, 'text': 'b'}]]:
            with self.subTest(captions=captions), self.assertRaises(ValueError):
                voice.validate_captions(captions, 2000)

    def test_ducking_follows_voice_and_recovers_in_pause(self):
        sr = voice.audio.SR
        speech = np.zeros((4 * sr, 2), dtype=np.float32)
        speech[sr:2 * sr] = 0.2
        music = np.full_like(speech, 0.1)
        mixed, evidence = voice.mix(speech, music, -6, -12)
        bed = mixed - speech
        during = np.mean(bed[int(1.3 * sr):int(1.7 * sr)])
        after = np.mean(bed[int(2.4 * sr):int(2.8 * sr)])
        self.assertLess(during, after * 0.3)
        self.assertAlmostEqual(evidence['duckMinimumDb'], -12, places=4)
        self.assertEqual(mixed.shape, speech.shape)

    def test_peak_headroom_and_silent_voice(self):
        loud = np.full((4800, 2), 0.99)
        result, _ = voice.mix(loud, loud, 0, -1)
        self.assertLessEqual(float(np.max(np.abs(result))), 10 ** (-1 / 20) + 1e-6)
        with self.assertRaises(ValueError): voice.mix(loud * 0, None)
        with self.assertRaises(ValueError): voice.mix(loud, loud, 2, -12)


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.now(timezone.utc)
        self.data = {'appVersion': 'synthetic-test', 'recorderState': 'idle', 'output': 'new.mp4',
            'target': {'app': 'Fixture', 'title': 'Unique fixture', 'sourceId': 'window:42', 'matches': 1,
                'width': 1920, 'height': 1080, 'minimumWidth': 1920, 'minimumHeight': 1080},
            'checks': {name: {'status': 'pass', 'observedAt': self.now.isoformat(), 'evidence': 'Synthetic observation for unit test'}
                for name in ['screenPermission', 'accessibilityPermission', 'source', 'resolution', 'export', 'idle']}}

    def test_ready_means_only_ready_to_attempt(self):
        self.assertEqual(capture.assess(self.data, self.now), [])

    def test_malformed_observations_fail_without_crashing(self):
        for data in [None, [], {'checks': []}, {'checks': None}, {'target': []},
            {'checks': {'source': None}}, {'checks': {'source': {'status': 'pass', 'evidence': 7, 'observedAt': 0}}}]:
            with self.subTest(data=data):
                self.assertTrue(capture.assess(data, self.now))
        data = copy.deepcopy(self.data)
        data['checks']['source']['observedAt'] = self.now.replace(tzinfo=None).isoformat()
        self.assertIn('source: require an ISO timestamp with timezone', capture.assess(data, self.now))

    def test_missing_stale_and_future_observations_fail(self):
        for name in self.data['checks']:
            for seconds in [-301, 1]:
                data = copy.deepcopy(self.data)
                data['checks'][name]['observedAt'] = (self.now + timedelta(seconds=seconds)).isoformat()
                self.assertTrue(capture.assess(data, self.now))
            data = copy.deepcopy(self.data)
            data['checks'][name]['status'] = 'unknown'
            self.assertTrue(capture.assess(data, self.now))

    def test_ambiguous_small_active_and_unknown_fail(self):
        for matches in [0, 2]:
            data = copy.deepcopy(self.data)
            data['target']['matches'] = matches
            self.assertTrue(capture.assess(data, self.now))
        for state in ['recording', 'exporting', 'unknown']:
            data = copy.deepcopy(self.data)
            data['recorderState'] = state
            self.assertTrue(capture.assess(data, self.now))
        data = copy.deepcopy(self.data)
        data['target']['width'] = 1280
        self.assertTrue(capture.assess(data, self.now))
        self.assertTrue(capture.assess({}, self.now))

    def test_cli_preserves_existing_media_and_reports_destination_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            input_file = root / 'observations.json'
            for label, output, expected in [('ready', root / 'new.mp4', 0),
                ('exists', root / 'existing.mp4', 1), ('missing', root / 'absent' / 'new.mp4', 1)]:
                preserved = root / 'existing.mp4'
                preserved.write_bytes(b'original take')
                self.data['output'] = str(output)
                input_file.write_text(json.dumps(self.data))
                report = root / f'{label}.json'
                result = subprocess.run([sys.executable, str(Path(__file__).with_name('capture-preflight.py')),
                    str(input_file), '--out', str(report)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertEqual(json.loads(report.read_text())['status'], 'READY_TO_ATTEMPT' if expected == 0 else 'NOT_READY')
                self.assertEqual(json.loads(report.read_text())['output'], str(output.resolve()))
                self.assertEqual(preserved.read_bytes(), b'original take')


if __name__ == '__main__':
    unittest.main()
