"""Validate fresh UI observations before recording; this script never controls the recorder.

python scripts/capture-preflight.py capture-observations.json --out readiness.json
Exit 0 = ready to attempt recording; 1 = not ready. Neither means a take was captured.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile


def assess(data, now=None):
    now = now or datetime.now(timezone.utc)
    if not isinstance(data, dict):
        return ['input: observations must be a JSON object']
    errors = []
    checks = data.get('checks')
    if not isinstance(checks, dict):
        checks = {}
    for name in ['screenPermission', 'accessibilityPermission', 'source', 'resolution', 'export', 'idle']:
        observation = checks.get(name)
        if not isinstance(observation, dict):
            observation = {}
        evidence = observation.get('evidence')
        if observation.get('status') != 'pass' or not isinstance(evidence, str) or not evidence.strip():
            errors.append(f'{name}: require a passed observation with evidence')
        try:
            observed = datetime.fromisoformat(observation['observedAt'].replace('Z', '+00:00'))
            age = (now - observed).total_seconds()
            if not 0 <= age <= 300:
                errors.append(f'{name}: observation is stale or in the future')
        except (KeyError, ValueError, TypeError, AttributeError):
            errors.append(f'{name}: require an ISO timestamp with timezone')
    target = data.get('target', {})
    if not isinstance(target, dict):
        target = {}
    if not all(isinstance(target.get(k), str) and target[k].strip() for k in ['app', 'title', 'sourceId']):
        errors.append('source: require the observed app, exact window title and source identifier')
    if type(target.get('matches')) is not int or target['matches'] != 1:
        errors.append('source: require exactly one matching window; never select the first display')
    for k in ['width', 'height', 'minimumWidth', 'minimumHeight']:
        if type(target.get(k)) is not int or target[k] <= 0:
            errors.append(f'resolution: {k} must be a positive integer')
    if not any(e.startswith('resolution:') for e in errors):
        if target['width'] < target['minimumWidth'] or target['height'] < target['minimumHeight']:
            errors.append('resolution: source is below the planned capture size')
    if data.get('recorderState') != 'idle':
        errors.append('idle: recording/export is active or unknown; inspect before retrying')
    if not isinstance(data.get('appVersion'), str) or not data['appVersion'].strip():
        errors.append('appVersion: inspect the installed version')
    if not isinstance(data.get('output'), str) or not data['output'].strip():
        errors.append('output: require a new local filename')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('observations', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.observations.read_text())
    errors = assess(data)
    destination = None
    if isinstance(data, dict) and isinstance(data.get('output'), str) and data['output'].strip():
        path = Path(data['output']).expanduser()
        if not path.is_absolute():
            path = args.observations.parent / path
        path = path.resolve()
        destination = str(path)
        if path.exists():
            errors.append('output: path already exists; preserve the prior export')
        else:
            try:
                with tempfile.TemporaryFile(dir=path.parent):
                    pass
            except OSError as error:
                errors.append(f'output: destination is not writable: {error}')
    report = {'status': 'READY_TO_ATTEMPT' if not errors else 'NOT_READY', 'errors': errors, 'output': destination,
        'checkedAt': datetime.now(timezone.utc).isoformat(),
        'basis': 'Operator/tool observations; permissions and UI state are not independently queried by this script.',
        'next': 'Re-observe source and idle state immediately before starting; require an active timer afterward.'}
    with args.out.open('x') as handle:
        json.dump(report, handle, indent=2)
    print(json.dumps(report))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
