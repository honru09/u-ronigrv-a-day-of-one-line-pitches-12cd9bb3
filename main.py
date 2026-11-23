"""Write the one-line pitch for the make.fun bounty
"A Day of One-Line Pitches" to /output/entry.txt.

The entry is a single sentence meant to convince a friend who has
never coded to let an AI agent build their first app idea on make.fun.
Deterministic, standard library only, no network, no randomness, no
clock reads: the same input always produces the same file.
"""

import os
import sys

ENTRY = (
    "You already have the hard part \u2014 the idea \u2014 so hand it to "
    "an AI agent on make.fun and it'll build your first app for you, "
    "free to try, no code required."
)

MIN_CHARS = 1
MAX_CHARS = 240


def validate(text):
    """Gate: 1-240 characters, not only whitespace. Exit non-zero otherwise."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        print(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text)),
            file=sys.stderr,
        )
        return False
    if not text.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return False
    return True


def clear_contents(out_dir):
    """Clear only the contents of the output dir, never the dir itself."""
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            clear_contents(path)
            os.rmdir(path)
        else:
            os.remove(path)


def main():
    if not validate(ENTRY):
        sys.exit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    clear_contents(out_dir)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)
    os.chmod(target, 0o644)


if __name__ == "__main__":
    main()
