#!/usr/bin/env python3
"""One Line of Earned Pride — make.fun entry.

Writes a single calibrated line of text (1-240 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Version history:
- v1: initial pick, calibrated against the judge brief (see NOTES.md
  in the work directory): lifetime arc, concrete scene, payoff on the
  last words, fresh image (piano mover, not trophy/podium/graduation).
- v2: gate also rejects ASCII control characters and double spaces
  (either would break the one-read landing), and main() reads the
  written file back and verifies it byte for byte before exiting 0.

Standard library only. Deterministic: the same bytes on every run.
"""

import os
import sys

ENTRY = (
    "All his life he carried other people's pianos up four flights; "
    "tonight he sat at one of his own and played the first bar "
    "without looking down."
)


def gate(text):
    """Self-check matching the competition gate: 1-240 chars, UTF-8,
    one line, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= 240):
        raise ValueError(f"entry length {len(text)} outside 1-240")
    if text != text.strip():
        raise ValueError("entry has leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry is not a single line")
    if any(ord(c) < 0x20 for c in text):
        raise ValueError("entry contains a control character")
    if "  " in text:
        raise ValueError("entry contains a double space")
    text.encode("utf-8")
    return True


def main():
    gate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(path, "r", encoding="utf-8", newline="") as f:
        if f.read() != ENTRY:
            raise ValueError("written entry does not round-trip")
    return 0


if __name__ == "__main__":
    sys.exit(main())
