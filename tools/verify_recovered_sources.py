#!/usr/bin/env python3
"""Verify every byte of the recovered source snapshot; optionally restore split files."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / '15_archive/recovery_2026_11_19/source_manifest.json'


def within(root: Path, relative: str) -> Path:
    value = (root / relative).resolve()
    if not value.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes source root: {relative}')
    return value


def verify(manifest_path: Path, restore: Path | None = None) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    checked = 0
    byte_count = 0
    for entry in manifest['sources']:
        whole = hashlib.sha256()
        total = 0
        destination = None
        temporary = None
        output = None
        if restore is not None:
            restore.mkdir(parents=True, exist_ok=True)
            destination = within(restore, entry['filename'])
            destination.parent.mkdir(parents=True, exist_ok=True)
            output = tempfile.NamedTemporaryFile(dir=destination.parent, delete=False)
            temporary = Path(output.name)
        try:
            for part in entry['parts']:
                path = within(ROOT, part['path'])
                digest = hashlib.sha256()
                size = 0
                with path.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        digest.update(block)
                        whole.update(block)
                        size += len(block)
                        if output is not None:
                            output.write(block)
                if size != part['size_bytes'] or digest.hexdigest() != part['sha256']:
                    raise ValueError(f'Part integrity failure: {part["path"]}')
                total += size
            if total != entry['size_bytes'] or whole.hexdigest() != entry['sha256']:
                raise ValueError(f'Source integrity failure: {entry["filename"]}')
            if output is not None:
                output.close()
                if destination.exists():
                    existing = hashlib.sha256(destination.read_bytes()).hexdigest()
                    if existing != entry['sha256']:
                        raise ValueError(f'Refusing to replace a different file: {destination}')
                    temporary.unlink()
                else:
                    os.replace(temporary, destination)
            checked += 1
            byte_count += total
        finally:
            if output is not None and not output.closed:
                output.close()
            if temporary is not None and temporary.exists():
                temporary.unlink()
    if checked != manifest['source_count'] or byte_count != manifest['total_source_bytes']:
        raise ValueError('Manifest totals differ from verified sources')
    return {'status': 'PASS', 'source_count': checked, 'verified_bytes': byte_count,
            'source_manifest': str(manifest_path.relative_to(ROOT)),
            'restored': restore is not None}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT)
    parser.add_argument('--restore', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.manifest, args.restore)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding='utf-8')
    print(encoded, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
