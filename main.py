#!/usr/bin/env python3
"""The Painfully Honest Out-of-Office.

Writes one brutally honest but still polite out-of-office auto-reply --
a single sentence of 1-200 characters -- to ``entry.txt`` inside the
output directory named by MAKEFUN_OUTPUT_DIR (default ``/output``).

The grader runs this program with a read-only filesystem, so nothing is
written anywhere except the output directory.
"""

import os
import sys

ENTRY = (
    "I'm away and honestly relieved to be unreachable, so your email "
    "will wait among 847 unread messages until I return with fresh patience."
)


def validate(text):
    """Check the entry against the bounty gate. Returns an error string or None."""
    if not text or not text.strip():
        return "entry is empty or only whitespace"
    if not 1 <= len(text) <= 200:
        return "entry is %d characters, must be 1-200" % len(text)
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if text[-1] not in ".!?":
        return "entry does not end with sentence punctuation"
    for sep in (". ", "! ", "? "):
        if sep in text:
            return "entry contains more than one sentence"
    if text.count(".") + text.count("!") + text.count("?") != 1:
        return "entry must be exactly one sentence"
    if any(ord(ch) < 32 for ch in text):
        return "entry contains a control character"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    return None


def main():
    error = validate(ENTRY)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)

    # Read-back verification: what the grader will read must be exactly the entry.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        print("read-back mismatch: entry.txt does not match the entry", file=sys.stderr)
        return 1

    print("wrote %d characters to %s" % (len(ENTRY), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
