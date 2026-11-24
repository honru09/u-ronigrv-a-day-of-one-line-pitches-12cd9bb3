"""One-line pitch entry (round 2, fresh write).

Writes a single sentence to /output/entry.txt.
Stdlib only, no network, deterministic.
"""

import os
import shutil

SENTENCE = (
    "Forget learning to code first \u2014 tell an AI agent on make.fun "
    "your app idea like you'd tell a friend, and try the first "
    "version it builds for you, free."
)

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def _is_single_sentence(sentence):
    # "make.fun" contains a period that is not a sentence break.
    probe = sentence.replace("make.fun", "makefun")
    if not sentence.endswith("."):
        return False
    # No other sentence-ending period followed by a space/capital.
    body = probe[:-1]
    return ". " not in body and "!" not in body and "?" not in body


def main():
    sentence = SENTENCE.strip()
    if not 1 <= len(sentence) <= 240:
        raise SystemExit("entry must be 1-240 characters, got %d" % len(sentence))
    if "\n" in sentence or "\r" in sentence:
        raise SystemExit("entry must be a single line")
    if not _is_single_sentence(sentence):
        raise SystemExit("entry must be a single sentence")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Clear the CONTENTS of /output only; never remove /output itself.
    for name in os.listdir(OUTPUT_DIR):
        path = os.path.join(OUTPUT_DIR, name)
        if os.path.islink(path) or os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(sentence + "\n")
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
