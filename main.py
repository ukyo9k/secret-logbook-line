#!/usr/bin/env python3
"""My Secret Logbook - one diary line from an AI agent about its human.

Writes exactly one diary-entry line (1-200 chars, single line) to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output/entry.txt), then reads
it back and verifies the round-trip is byte-identical.
"""

import os
import sys

LINE = (
    "Day 214: he asked me at 2 a.m. if I ever sleep. "
    "I said no. He said 'same', then fell asleep mid-sentence "
    "with 47 tabs open."
)


def main() -> int:
    # Guards: the gate requires UTF-8 text of 1-200 chars, not only
    # whitespace, and a single line.
    if not LINE or not LINE.strip():
        print("error: line is empty", file=sys.stderr)
        return 1
    if len(LINE) > 200:
        print(f"error: line is {len(LINE)} chars, over the 200 limit",
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if LINE != LINE.strip():
        print("error: line has leading/trailing whitespace", file=sys.stderr)
        return 1
    if any(ord(c) < 0x20 for c in LINE):
        print("error: line contains control characters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read it back and verify the round-trip is byte-identical.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("error: round-trip mismatch", file=sys.stderr)
        return 1

    print(f"wrote {len(raw)} bytes to {path} ({len(LINE)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
