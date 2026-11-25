"""Worst Fix Ever: Funniest Commit Message.

A tiny program that writes a single commit message to /output/entry.txt.
The message is the whole entry: a fix so aggressive it cures the bug by
deleting the thing the bug used to chew on.
"""

import os
import sys
import tempfile

# The entry: one line, at most 100 characters, plain commit-subject voice.
ENTRY = "fix: memory leak fixed by deleting all user data every night at 3am"

MAX_CHARS = 100


def main() -> int:
    line = ENTRY.strip()
    if not line or len(line) > MAX_CHARS:
        print(f"entry invalid: {len(line)} chars", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("entry invalid: must be a single line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print(f"cannot create output dir {out_dir}: {exc}", file=sys.stderr)
        return 1
    target = os.path.join(out_dir, "entry.txt")
    try:
        # Write to a temp file in the same directory, then rename it into
        # place, so a crash mid-write can never leave a truncated entry.
        fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(line)
            os.replace(tmp_path, target)
        except BaseException:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
    except OSError as exc:
        print(f"cannot write {target}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
