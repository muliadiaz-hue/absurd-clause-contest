#!/usr/bin/env python3
"""The Absurd Clause Contest entry.

Writes one absurd terms-of-service clause to ``entry.txt`` inside the
output directory. The grader reads that file and judges the text; the
program itself is deliberately tiny and deterministic so both graded
runs produce byte-identical output.
"""

import os
import sys

# The clause: a deadpan IP-assignment paragraph whose absurdity only
# lands on the last phrase — the Company owns the chapters not yet lived.
CLAUSE = (
    "The User hereby assigns to the Company all rights in the User's "
    "autobiography, including the chapters the User has not yet lived."
)

FILENAME = "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def output_dir() -> str:
    """Where the entry goes: the harness dir when set, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def check_clause(text: str) -> None:
    """Enforce the competition gate before anything is written."""
    if not text or not text.strip():
        raise ValueError("clause must not be empty or whitespace only")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"clause is {len(text)} chars, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def main() -> int:
    check_clause(CLAUSE)
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, FILENAME)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(CLAUSE)
    # Self-check: what landed on disk must be exactly the validated clause,
    # so a partial write can never silently pass as a valid entry.
    with open(target, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != CLAUSE:
            raise RuntimeError(f"{target} does not match the clause")
    print(f"wrote {len(CLAUSE)} chars to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
