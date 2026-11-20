#!/usr/bin/env python3
"""Lossless, documented Google Docs -> Lean *transport* cleanup.

Preserve original source files unchanged. Create separate compiler copies after
removing only an initial UTF-8 BOM, a leading filename heading, and two known
Google Docs code-block presentation markers. The manifest records every change.
Theorem statements, proofs, constants, and declarations are not edited.
"""
import argparse
import hashlib
import json
import pathlib


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    src = pathlib.Path(args.src)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    entries = []
    for path in sorted(src.glob("*.lean")):
        raw = path.read_bytes()
        changes = []
        bom = raw.startswith(b"\xef\xbb\xbf")
        text = raw.decode("utf-8-sig")
        if bom:
            changes.append("removed leading UTF-8 byte-order mark")
        first, sep, rest = text.partition("\n")
        if first.strip() == path.name and sep:
            text = rest
            changes.append("removed leading Google Docs filename display line")
        for marker, label in [("\uec03", "Google Docs code-block start marker"),
                              ("\uec02", "Google Docs code-block end marker")]:
            count = text.count(marker)
            if count:
                text = text.replace(marker, "")
                changes.append(f"removed {count} {label}(s)")
        normalized = text.encode("utf-8")
        (out / path.name).write_bytes(normalized)
        entries.append({
            "file": path.name,
            "original_sha256": digest(raw),
            "compiled_copy_sha256": digest(normalized),
            "transport_only_changes": changes,
        })
    (out / "TRANSPORT_NORMALIZATION_MANIFEST.json").write_text(
        json.dumps({"count": len(entries), "note": "No theorem or proof expressions changed", "files": entries}, indent=2) + "\n"
    )
    print(f"Prepared {len(entries)} separate Lean compiler copies; originals untouched")
    for e in entries:
        if e["transport_only_changes"]:
            print(e["file"], ":", "; ".join(e["transport_only_changes"]))


if __name__ == "__main__":
    main()
