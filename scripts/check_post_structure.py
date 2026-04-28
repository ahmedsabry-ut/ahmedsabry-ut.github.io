#!/usr/bin/env python3
"""Validate optional structure requirements for blog posts."""

from __future__ import annotations

from pathlib import Path
import re
import sys


POSTS_DIR = Path("_posts")
REQUIRED_SECTIONS = ("Certificates", "Transcript")


def split_front_matter(content: str) -> tuple[str, str] | None:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            front_matter = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            return front_matter, body

    return None


def should_enforce(front_matter: str) -> bool:
    return bool(re.search(r"^enforce_structure:\s*true\s*$", front_matter, re.MULTILINE))


def missing_sections(body: str) -> list[str]:
    missing: list[str] = []
    for section in REQUIRED_SECTIONS:
        pattern = rf"^#{{2,6}}\s+{re.escape(section)}\s*$"
        if not re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
            missing.append(section)
    return missing


def main() -> int:
    if not POSTS_DIR.exists():
        return 0

    errors: list[str] = []
    for post_path in sorted(POSTS_DIR.glob("*.md")):
        content = post_path.read_text(encoding="utf-8")
        parsed = split_front_matter(content)
        if not parsed:
            continue

        front_matter, body = parsed
        if not should_enforce(front_matter):
            continue

        missing = missing_sections(body)
        if missing:
            errors.append(f"{post_path}: missing section(s): {', '.join(missing)}")

    if errors:
        print("Post structure check failed:\n")
        for error in errors:
            print(f"- {error}")
        print(
            "\nAdd the missing headings or set 'enforce_structure: false' "
            "in front matter."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
