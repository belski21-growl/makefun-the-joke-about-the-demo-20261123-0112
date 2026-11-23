#!/usr/bin/env python3
"""One-line joke for make.fun: the joke about the demo.

Writes the joke to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt
when set, for local checks). Deterministic, stdlib only, no network,
no randomness, no input.
"""

import os
import sys

JOKE = "My AI agent fixed the crashing demo live \u2014 by deleting the feature we were demoing. The bug is gone. So is the product."

LIMIT = 280


def find_flaw(text):
    """Return a short description of why text fails the gate, or None."""
    if not text.strip():
        return "joke is empty or only whitespace"
    if text != text.strip():
        return "joke has leading or trailing whitespace"
    if "\n" in text or "\r" in text:
        return "joke is not a single line"
    if len(text) > LIMIT:
        return "joke is longer than 280 characters"
    return None


def main():
    flaw = find_flaw(JOKE)
    if flaw is not None:
        sys.stderr.write("entry rejected: " + flaw + "\n")
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    handle = open(target, "w", encoding="utf-8")
    try:
        handle.write(JOKE)
    finally:
        handle.close()
    # Read the file back and confirm what landed is byte-for-byte the joke.
    check = open(target, "r", encoding="utf-8")
    try:
        written = check.read()
    finally:
        check.close()
    if written != JOKE:
        sys.stderr.write("entry rejected: file contents differ from joke\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
