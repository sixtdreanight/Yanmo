import re
from dataclasses import dataclass


@dataclass
class BibEntry:
    entry_type: str
    cite_key: str
    title: str = ""
    author: str = ""
    year: str = ""
    journal: str = ""
    booktitle: str = ""
    raw: str = ""


def _extract_braced_block(text: str, start: int) -> tuple[str, int] | None:
    """Return (content_inside_braces, pos_after_closing) starting from start
    which should point at the opening '{'."""
    if start >= len(text) or text[start] != "{":
        return None
    depth = 1
    i = start + 1
    while i < len(text) and depth > 0:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    if depth != 0:
        return None
    return text[start + 1 : i - 1], i


def parse_bibtex(text: str) -> list[BibEntry]:
    entries: list[BibEntry] = []
    i = 0

    while i < len(text):
        # Look for @type{
        m = re.compile(r"@(\w+)\s*\{").search(text, i)
        if not m:
            break

        entry_type = m.group(1)
        after_brace = m.end()  # position right after the opening '{'

        # Find the comma that ends the cite key
        comma_pos = text.find(",", after_brace)
        if comma_pos == -1:
            break

        cite_key = text[after_brace:comma_pos].strip()

        # Extract the full braced block content
        result = _extract_braced_block(text, m.end() - 1)
        if result is None:
            break
        full_body, next_i = result

        # Body text is everything after the cite key and comma
        body_text = ""
        key_comma_end = full_body.find(",")
        if key_comma_end != -1:
            body_text = full_body[key_comma_end + 1:].strip()

        entry = BibEntry(entry_type=entry_type, cite_key=cite_key)
        entry.raw = f"@{entry_type}{{{cite_key}, ...}}"

        # Parse fields from body_text using brace-counting extraction
        for field_name in ["title", "author", "journal", "booktitle"]:
            pat = re.compile(rf"{field_name}\s*=\s*\{{")
            match = pat.search(body_text)
            if match:
                result = _extract_braced_block(body_text, match.end() - 1)
                if result:
                    setattr(entry, field_name, result[0].strip())

        year_match = re.search(r'year\s*=\s*\{?(\d{4})\}?', body_text)
        if year_match:
            entry.year = year_match.group(1)

        entries.append(entry)
        i = next_i

    return entries
