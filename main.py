#!/usr/bin/env python3
"""Warning Label for Humans: One Line, Big Laugh.

Writes the single-line safety warning label to
$MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic, stdlib only, no network.
"""

import os
import sys

ENTRY = (
    "WARNING: Contains one human. May say 'I'm on my way' from bed, "
    "lose the phone it is holding, and blame the Wi-Fi for decisions "
    "it made itself."
)


def main() -> int:
    # Self-check: exactly one non-blank line, 1-160 chars (UTF-8).
    if not ENTRY or not ENTRY.strip():
        print("error: entry is blank", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("error: entry must be exactly one line", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip():
        print("error: entry must not have leading/trailing whitespace",
              file=sys.stderr)
        return 1
    # Count in characters, but also guard the UTF-8 byte length stays sane.
    if len(ENTRY.encode("utf-8")) > 160 * 4:
        print("error: entry UTF-8 encoding unexpectedly long",
              file=sys.stderr)
        return 1
    if len(ENTRY) > 160:
        print(
            f"error: entry is {len(ENTRY)} chars, over the 160 limit",
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")

    # Verify what was written matches the entry exactly.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY + "\n":
        print("error: written output does not match entry", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
