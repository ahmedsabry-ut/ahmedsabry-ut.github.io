#!/usr/bin/env python3
"""Ensure first GE Vernova mention includes parenthetical expansion."""

from __future__ import annotations

from pathlib import Path
import re
import sys


POSTS_DIR = Path("_posts")
FIRST_MENTION_REQUIRED = "GE Vernova (General Electric)"
MENTION_PATTERN = re.compile(r"GE Vernova(?:\s*\(General Electric\))?")


def main() -> int:
    if not POSTS_DIR.exists():
        return 0

    errors: list[str] = []

    for post_path in sorted(POSTS_DIR.glob("*.md")):
        content = post_path.read_text(encoding="utf-8")
        match = MENTION_PATTERN.search(content)
        if not match:
            continue

        first_mention = match.group(0)
        if first_mention != FIRST_MENTION_REQUIRED:
            errors.append(
                f"{post_path}: first mention must be '{FIRST_MENTION_REQUIRED}'"
            )

    if errors:
        print("GE Vernova first-mention check failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
