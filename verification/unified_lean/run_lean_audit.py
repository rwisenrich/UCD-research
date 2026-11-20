#!/usr/bin/env python3
"""Compile every original Lean theorem source independently, retaining all diagnostics.

This is a compiler audit, not a proof-scope equivalence certificate.
Only pure source files are checked; original source bytes are never modified.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from datetime import datetime, timezone


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--cwd", default=".")
    p.add_argument("--seconds", type=int, default=180)
    args = p.parse_args()

    root = pathlib.Path(args.root).resolve()
    out = pathlib.Path(args.output).resolve()
    cwd = pathlib.Path(args.cwd).resolve()
    out.mkdir(parents=True, exist_ok=True)
    sources = sorted(s for s in root.rglob("*.lean")
                     if s.is_file() and not s.name.lower().endswith("lakefile.lean"))
    if not sources:
        raise SystemExit(f"No proof-source .lean files found under {root}")

    rows = []
    for idx, src in enumerate(sources, 1):
        rel = src.relative_to(root).as_posix()
        payload = src.read_bytes()
        sha = hashlib.sha256(payload).hexdigest()
        normalized = rel.replace("/", "__")
        log = out / f"{normalized}.log"
        try:
            r = subprocess.run(
                ["lean", str(src)], cwd=cwd, capture_output=True,
                text=True, errors="replace", timeout=args.seconds
            )
            status = "pass" if r.returncode == 0 else "fail"
            exit_code = r.returncode
            stdout = r.stdout + r.stderr
        except subprocess.TimeoutExpired as e:
            status = "timeout"
            exit_code = 124
            stdout = str(e.stdout or b"") + "\n" + str(e.stderr or b"")
        except OSError as e:
            status = "tool-error"
            exit_code = 127
            stdout = str(e)
        log.write_text(stdout, encoding="utf-8", errors="replace")
        source_text = payload.decode("utf-8", errors="replace")
        # Lexical counts include comments; they are triage flags, not proof certification.
        rows.append({
            "file": rel, "sha256": sha, "status": status, "exit_code": exit_code,
            "declaration_lines": len(re.findall(
                r"(?m)^\s*(?:(?:private|protected|noncomputable)\s+)*(?:theorem|lemma)\s+",
                source_text
            )),
            "raw_sorry_tokens": len(re.findall(r"\bsorry\b", source_text)),
            "raw_axiom_tokens": len(re.findall(r"\baxiom\b", source_text)),
            "log": log.name,
        })
        print(f"[{idx:03d}/{len(sources):03d}] {status.upper():7s} {rel}", flush=True)

    totals = {
        "total": len(rows),
        "pass": sum(r["status"] == "pass" for r in rows),
        "fail": sum(r["status"] == "fail" for r in rows),
        "timeout": sum(r["status"] == "timeout" for r in rows),
        "tool_error": sum(r["status"] == "tool-error" for r in rows),
    }
    report = {
        "audit": "UCD independent original-source Lean compiler audit",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "scope": str(root),
        "toolchain": subprocess.run(
            ["lean", "--version"], capture_output=True, text=True
        ).stdout.strip(),
        "disclaimer": "Compiler success does not establish manuscript theorem scope, physical predictions, or absence of extra axioms. Raw lexical tokens include comments.",
        "totals": totals,
        "files": rows,
    }
    (out / "summary.json").write_text(json.dumps(report, indent=2) + "\n")
    with (out / "summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("TOTALS", json.dumps(totals), flush=True)
    return 0 if totals["pass"] == totals["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
