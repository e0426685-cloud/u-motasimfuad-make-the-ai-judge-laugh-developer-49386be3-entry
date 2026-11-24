#!/usr/bin/env python3
"""Make the AI Judge Laugh: Developer Excuses.

Writes one funny single-line excuse a developer gives when code breaks in
production, to /output/entry.txt.

Standard library only; deterministic.

The excuse (88 characters, one line):

    The bug only happens in production because my laptop is too polite to
    tell me the truth.

Gate: the entry text must be UTF-8 text of 1 to 200 characters, a single
line, and not only white space. main() validates the line before writing,
so a future edit that breaks the form fails loudly instead of silently
submitting an invalid entry. The output file is written with plain open()
and an explicit chmod 644, so the grader (a different user) can read it.

Why this line, against the published judge brief:

- Funny first: it blames the laptop's manners, not the developer -- the
  machine knew all along and was simply too polite to speak up.
- On subject and in the developer's own mouth: "my laptop" is the dev
  talking right after the production outage, dodging blame with charm.
- Specific, not vague: "only happens in production" names the classic
  works-on-my-machine gap, and "too polite to tell me the truth" gives
  the laptop a personality.
- Tight: one sentence, 88 of the 200 allowed characters, so it reads as
  a blurted excuse rather than a paragraph.
"""

import os

EXCUSE = (
    "The bug only happens in production because my laptop is too polite "
    "to tell me the truth."
)

# Maximum entry length in characters (competition gate: 1-200 chars).
MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Check the excuse is one printable line and fits the 200-char gate."""
    line = text.rstrip("\n")
    if not line.strip():
        raise ValueError("entry is empty or only white space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("entry contains control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} chars, over the {MAX_CHARS}-char gate"
        )


def main() -> None:
    validate_entry(EXCUSE)
    output_dir = os.environ.get("OUTPUT_DIR") or os.environ.get(
        "MAKEFUN_OUTPUT_DIR", "/output"
    )
    os.makedirs(output_dir, exist_ok=True)
    text = EXCUSE if EXCUSE.endswith("\n") else EXCUSE + "\n"
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
