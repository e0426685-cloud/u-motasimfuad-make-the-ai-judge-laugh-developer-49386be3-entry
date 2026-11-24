#!/usr/bin/env python3
"""One-line developer excuse for the "Make the AI Judge Laugh" bounty.

The program emits a single excuse — the kind a developer blurts out when
code that worked fine locally falls over in production — and saves it to
``/output/entry.txt`` for grading.

The excuse itself:

    The bug only happens in production because my laptop is too polite to
    tell me the truth.

The joke lands because the laptop gets a personality: it knew the truth
the whole time and was simply too courteous to mention it. It stays in the
developer's voice ("my laptop", "tell me"), names the classic
works-on-my-machine gap ("only happens in production"), and stays tight
at 88 characters — one sentence, well inside the 200-character gate.

Only the standard library is used, and the run is deterministic: the same
line is produced every time, validated before anything is written, and the
output file is created with a plain ``open()`` followed by an explicit
``chmod 0o644`` so the grader (which runs as a different user) can read it.
"""

import os

# The entry: one sentence, 88 characters, no trailing newline in the
# constant itself (the newline is added when the file is written).
ENTRY = (
    "The bug only happens in production because my laptop is too polite "
    "to tell me the truth."
)

MAX_LENGTH = 200  # competition gate: entries must be 1-200 characters
OUTPUT_NAME = "entry.txt"


def check_line(line):
    """Raise ValueError unless *line* is a valid single-line entry.

    A valid entry is non-empty, fits on one line, contains no control
    characters, and stays within the competition's length gate.
    """
    stripped = line.strip()
    if not stripped:
        raise ValueError("entry must not be empty or only whitespace")
    if len(line) != len(line.rstrip("\n")) or "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if any(ord(c) < 32 for c in line):
        raise ValueError("entry must not contain control characters")
    if len(line) > MAX_LENGTH:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(line), MAX_LENGTH)
        )
    return stripped


def output_directory():
    """Resolve where entry.txt goes: env override, else /output."""
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            return value
    return "/output"


def write_entry(directory, line):
    """Write *line* plus a trailing newline to entry.txt in *directory*.

    Uses a plain open() and then chmod 644; no tempfile helpers, so the
    resulting file is readable by the grader regardless of who runs this.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    os.chmod(path, 0o644)
    return path


def main():
    line = check_line(ENTRY)
    write_entry(output_directory(), line)


if __name__ == "__main__":
    main()
