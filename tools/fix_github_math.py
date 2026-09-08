#!/usr/bin/env python3
"""Normalize UCD Markdown to GitHub-native MathJax delimiters.

GitHub renders block math with $$ ... $$ (or fenced math blocks).  The UCD
research notes originally used LaTeX document delimiters \\[ ... \\], which
GitHub mobile displayed literally.  This tool converts only delimiter lines
outside fenced code blocks, so source examples remain untouched.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "node_modules"}


def iter_markdown(root: Path):
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def normalize(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_fence = False
    changes = 0
    fence_token = None

    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = None
            out.append(line)
            continue

        if not in_fence:
            body = line.rstrip("\r\n")
            ending = line[len(body):]
            indent = body[: len(body) - len(body.lstrip())]
            token = body.strip()
            if token == r"\[":
                out.append(indent + "$$" + ending)
                changes += 1
                continue
            if token == r"\]":
                out.append(indent + "$$" + ending)
                changes += 1
                continue

        out.append(line)

    return "".join(out), changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting")
    args = parser.parse_args()

    total = 0
    bad: list[str] = []
    for path in iter_markdown(ROOT):
        old = path.read_text(encoding="utf-8")
        new, n = normalize(old)
        if not n:
            continue
        total += n
        bad.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.write_text(new, encoding="utf-8")

    if args.check and bad:
        print("GitHub math delimiter violations:")
        for path in bad:
            print(f" - {path}")
        return 1

    print(f"normalized {total} block-math delimiter lines across {len(bad)} Markdown files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
