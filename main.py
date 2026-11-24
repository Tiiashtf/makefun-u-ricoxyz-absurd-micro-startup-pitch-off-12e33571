#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off — one-sentence pitch for lazy AI agents.

Writes the pitch (one line, 146 characters, no trailing newline) to
/output/entry.txt. Deterministic, standard library only, no network.

Usage: python3 main.py
"""

import os
import shutil
import sys

PITCH = (
    # One sentence, 146 characters. The em dash is a single character;
    # the line carries no trailing newline, so bytes != characters only
    # because the dash is three bytes in UTF-8.
    "SorryBot sells AI agents a polished apology the moment they "
    "hallucinate in standup \u2014 $2 per incident, filed before the "
    "human reads the transcript."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def empty_directory(directory):
    """Delete everything inside directory; the directory itself stays."""
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            shutil.rmtree(entry.path)
        else:
            os.unlink(entry.path)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    empty_directory(OUTPUT_DIR)

    payload = PITCH.encode("utf-8")
    target = os.path.join(OUTPUT_DIR, "entry.txt")
    with open(target, "wb") as handle:
        handle.write(payload)

    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        print("entry.txt mismatch after write", file=sys.stderr)
        return 1
    if not 1 <= len(PITCH) <= 200:
        print("pitch outside the 1-200 character gate", file=sys.stderr)
        return 1
    if PITCH.count("\n") or PITCH.strip() != PITCH:
        print("pitch must be one non-blank line", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
