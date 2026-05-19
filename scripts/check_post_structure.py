#!/usr/bin/env python3
"""Validate optional structure requirements for blog posts."""

from __future__ import annotations

from pathlib import Path
import re
import sys


POSTS_DIR = Path("_posts")
REQUIRED_SECTIONS = ("Transcript",)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
POST_FILENAME_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})-.+\.md$")
CREDENTIAL_LINE = re.compile(
    r"The verified learning credential can be found \[here\]\((https?://[^)]+)\)",
    re.IGNORECASE,
)
PLACEHOLDER_URL = re.compile(
    r"insert|example\.com|example-certificate|REPLACE",
    re.IGNORECASE,
)
LIST_ITEM = re.compile(r"^\s*-\s+.+", re.MULTILINE)
TRANSCRIPT_SECTION = re.compile(
    r"^#{2,6}\s+Transcript\s*$([\s\S]*?)(?=^#{2,6}\s+|\Z)",
    re.MULTILINE | re.IGNORECASE,
)


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


def is_semester_post(front_matter: str) -> bool:
    return bool(re.search(r"^semester_post:\s*true\s*$", front_matter, re.MULTILINE))


def front_matter_value(front_matter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", front_matter, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def missing_sections(body: str) -> list[str]:
    missing: list[str] = []
    for section in REQUIRED_SECTIONS:
        pattern = rf"^#{{2,6}}\s+{re.escape(section)}\s*$"
        if not re.search(pattern, body, re.MULTILINE | re.IGNORECASE):
            missing.append(section)
    return missing


def transcript_section(body: str) -> str | None:
    match = TRANSCRIPT_SECTION.search(body)
    if not match:
        return None
    return match.group(1)


def line_has_valid_credential_link(line: str) -> bool:
    for match in CREDENTIAL_LINE.finditer(line):
        url = match.group(1).strip()
        if not url or url == "#":
            continue
        if PLACEHOLDER_URL.search(url):
            continue
        return True
    return False


def credential_list_errors(transcript_body: str) -> list[str]:
    errors: list[str] = []
    list_items = LIST_ITEM.findall(transcript_body)
    if not list_items:
        errors.append(
            "Transcript must include a credential list (markdown `- ` items, one per course)"
        )
        return errors

    for index, item in enumerate(list_items, start=1):
        if not line_has_valid_credential_link(item):
            errors.append(
                f"credential list item {index} must include "
                "'The verified learning credential can be found [here](https://...)' "
                "with a real URL (not a placeholder)"
            )
    return errors


def validate_semester_metadata(front_matter: str) -> list[str]:
    errors: list[str] = []

    if front_matter_value(front_matter, "title") is None:
        errors.append("missing 'title'")

    semester_raw = front_matter_value(front_matter, "semester")
    if semester_raw is None:
        errors.append("missing 'semester' (expected 1-8)")
    else:
        try:
            semester = int(semester_raw)
        except ValueError:
            errors.append(f"invalid 'semester' value: {semester_raw!r} (expected 1-8)")
        else:
            if not 1 <= semester <= 8:
                errors.append(f"invalid 'semester' value: {semester} (expected 1-8)")

    semester_end: str | None = None
    for date_key in ("semester_start", "semester_end"):
        value = front_matter_value(front_matter, date_key)
        if value is None:
            errors.append(f"missing {date_key!r}")
        elif not ISO_DATE.match(value):
            errors.append(f"invalid {date_key} {value!r} (expected YYYY-MM-DD)")
        elif date_key == "semester_end":
            semester_end = value

    publish_date = front_matter_value(front_matter, "date")
    if publish_date is None:
        errors.append("missing 'date'")
    elif not ISO_DATE.match(publish_date):
        errors.append(f"invalid date {publish_date!r} (expected YYYY-MM-DD)")
    elif semester_end is not None and publish_date != semester_end:
        errors.append(
            f"date {publish_date!r} must match semester_end {semester_end!r} "
            "(use the last day of the term month)"
        )

    return errors, publish_date


def validate_filename_date(post_path: Path, publish_date: str | None) -> list[str]:
    errors: list[str] = []
    match = POST_FILENAME_DATE.match(post_path.name)
    if not match:
        errors.append("filename must be YYYY-MM-DD-<slug>.md")
        return errors
    if publish_date is not None and match.group(1) != publish_date:
        errors.append(
            f"filename date {match.group(1)!r} must match date {publish_date!r}"
        )
    return errors


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
        if not is_semester_post(front_matter):
            continue

        metadata_errors, publish_date = validate_semester_metadata(front_matter)
        for error in metadata_errors:
            errors.append(f"{post_path}: {error}")

        for error in validate_filename_date(post_path, publish_date):
            errors.append(f"{post_path}: {error}")

        missing = missing_sections(body)
        if missing:
            errors.append(f"{post_path}: missing section(s): {', '.join(missing)}")

        section = transcript_section(body)
        if section is None:
            errors.append(f"{post_path}: missing ## Transcript section")
        else:
            for error in credential_list_errors(section):
                errors.append(f"{post_path}: {error}")

    if errors:
        print("Post structure check failed:\n")
        for error in errors:
            print(f"- {error}")
        print(
            "\nFix front matter, Transcript heading, credential link, and filename date, "
            "or set 'semester_post: false' in front matter."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
