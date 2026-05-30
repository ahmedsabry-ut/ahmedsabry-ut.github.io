#!/usr/bin/env python3
"""Validate optional structure requirements for blog posts."""

from __future__ import annotations

from pathlib import Path
import re
import sys


POSTS_DIR = Path("_posts")
DATA_DIR = Path("_data")
REQUIRED_SECTIONS = ("Transcript",)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
POST_FILENAME_DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})-.+\.md$")
CREDENTIAL_LINE = re.compile(
    r"The verified learning credential can be found \[here\]\((https?://[^)]+)\)",
    re.IGNORECASE,
)
PLACEHOLDER_URL = re.compile(
    r"insert|example\.com|example-certificate|REPLACE|PENDING",
    re.IGNORECASE,
)
CREDENTIAL_UNAVAILABLE = re.compile(
    r"The verified learning credential is not available\.?",
    re.IGNORECASE,
)
LIST_ITEM = re.compile(r"^[ \t]*-\s+.+", re.MULTILINE)
TRANSCRIPT_SECTION = re.compile(
    r"^#{2,6}\s+Transcript\s*$([\s\S]*?)(?=^#{2,6}\s+|\Z)",
    re.MULTILINE | re.IGNORECASE,
)
TRANSCRIPT_INCLUDE = re.compile(
    r"\{%\s*include\s+transcript-credentials\.html(?:\s+[^%]+)?\s*%\}",
    re.IGNORECASE,
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
    return front_matter_value(front_matter, "semester") is not None


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


def line_has_valid_credential_entry(line: str) -> bool:
    if CREDENTIAL_UNAVAILABLE.search(line):
        return True
    for match in CREDENTIAL_LINE.finditer(line):
        url = match.group(1).strip()
        if not url or url == "#":
            continue
        if PLACEHOLDER_URL.search(url):
            continue
        return True
    return False


def load_yaml_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        import yaml
    except ImportError:
        return _parse_simple_yaml_records(path.read_text(encoding="utf-8"))
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def _parse_simple_yaml_records(content: str) -> list[dict]:
    records: list[dict] = []
    current: dict | None = None
    for line in content.splitlines():
        if line.startswith("- "):
            if current:
                records.append(current)
            current = {}
            key, _, value = line[2:].partition(":")
            current[key.strip()] = _parse_simple_yaml_value(value.strip())
        elif line.startswith("  ") and current is not None:
            key, _, value = line.strip().partition(":")
            current[key.strip()] = _parse_simple_yaml_value(value.strip())
    if current:
        records.append(current)
    return records


def _parse_simple_yaml_value(raw: str):
    if raw in ("null", "~", ""):
        return None
    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw.isdigit():
        return int(raw)
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return raw[1:-1]
    return raw


def term_for_semester(semester: int) -> str | None:
    record = semester_record(semester)
    if record is None:
        return None
    term = record.get("term")
    return term if isinstance(term, str) else None


def semester_record(semester: int) -> dict | None:
    for record in load_yaml_records(DATA_DIR / "semesters.yml"):
        if record.get("number") == semester:
            return record
    return None


def courses_for_term(term: str) -> list[dict]:
    courses: list[dict] = []
    for course in load_yaml_records(DATA_DIR / "courses.yml"):
        if course.get("taken") and course.get("semester") == term:
            courses.append(course)
    return courses


def url_is_valid_credential(url: str) -> bool:
    if not url or url == "#":
        return False
    return not PLACEHOLDER_URL.search(url)


def credential_list_errors(transcript_body: str) -> list[str]:
    errors: list[str] = []
    list_items = LIST_ITEM.findall(transcript_body)
    if not list_items:
        if re.search(r"no courses", transcript_body, re.IGNORECASE):
            return errors
        errors.append(
            "Transcript must include a credential list (markdown `- ` items, one per course)"
        )
        return errors

    for index, item in enumerate(list_items, start=1):
        if not line_has_valid_credential_entry(item):
            errors.append(
                f"credential list item {index} must include either "
                "'The verified learning credential can be found [here](https://...)' "
                "with a real URL (not a placeholder), or "
                "'The verified learning credential is not available.'"
            )
    return errors


def transcript_include_errors(front_matter: str, transcript_body: str) -> list[str]:
    errors: list[str] = []
    if not TRANSCRIPT_INCLUDE.search(transcript_body):
        errors.append(
            "Transcript must include "
            "'{% include transcript-credentials.html %}' "
            "or a credential list (markdown `- ` items, one per course)"
        )
        return errors

    semester_raw = front_matter_value(front_matter, "semester")
    if semester_raw is None:
        errors.append("missing 'semester' required for transcript-credentials include")
        return errors

    try:
        semester = int(semester_raw)
    except ValueError:
        errors.append(f"invalid 'semester' value: {semester_raw!r}")
        return errors

    term = term_for_semester(semester)
    if term is None:
        errors.append(
            f"semester {semester} has no matching term in _data/semesters.yml"
        )
        return errors

    record = semester_record(semester)
    courses = courses_for_term(term)
    if not courses:
        if semester == 3:
            return errors
        errors.append(
            f"no taken courses in _data/courses.yml for term {term!r} "
            f"(semester {semester})"
        )
        return errors

    report_image = record.get("report_image") if record else None
    if not report_image:
        errors.append(
            f"semester {semester} must have report_image in _data/semesters.yml"
        )

    for index, course in enumerate(courses, start=1):
        code = course.get("code", "?")
        name = course.get("name", "?")
        url = course.get("credential_url")
        if url is None:
            continue
        if not isinstance(url, str) or not url_is_valid_credential(url):
            errors.append(
                f"credential for {code} — {name} (item {index}) must be a real URL "
                "(not a placeholder), or omit credential_url for unavailable"
            )
    return errors


def validate_transcript_section(front_matter: str, transcript_body: str) -> list[str]:
    if TRANSCRIPT_INCLUDE.search(transcript_body):
        return transcript_include_errors(front_matter, transcript_body)
    return credential_list_errors(transcript_body)


def validate_semester_metadata(front_matter: str) -> list[str]:
    errors: list[str] = []

    if front_matter_value(front_matter, "title") is None:
        errors.append("missing 'title'")

    semester_raw = front_matter_value(front_matter, "semester")
    semester_end: str | None = None
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
            else:
                record = semester_record(semester)
                if record is None:
                    errors.append(
                        f"semester {semester} has no matching row in _data/semesters.yml"
                    )
                else:
                    end = record.get("semester_end")
                    if not isinstance(end, str) or not ISO_DATE.match(end):
                        errors.append(
                            f"semester {semester} has invalid semester_end in "
                            "_data/semesters.yml"
                        )
                    else:
                        semester_end = end

    publish_date = front_matter_value(front_matter, "date")
    if publish_date is None:
        errors.append("missing 'date'")
    elif not ISO_DATE.match(publish_date):
        errors.append(f"invalid date {publish_date!r} (expected YYYY-MM-DD)")
    elif semester_end is not None and publish_date != semester_end:
        errors.append(
            f"date {publish_date!r} must match semester_end {semester_end!r} "
            "from _data/semesters.yml (use the last day of the term month)"
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
            for error in validate_transcript_section(front_matter, section):
                errors.append(f"{post_path}: {error}")

    if errors:
        print("Post structure check failed:\n")
        for error in errors:
            print(f"- {error}")
        print(
            "\nFix front matter, Transcript heading, credential link, and filename date, "
            "or remove 'semester' from front matter."
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
