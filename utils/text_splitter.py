from typing import List
import re


def split_text(text: str, chunk_size: int = 3000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks safely.
    Prevents infinite loops and handles small PDFs.
    """

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)

        # Try to end at a sentence boundary
        if end < text_length:
            break_point = text.rfind('.', start, end)
            if break_point != -1 and break_point > start + overlap:
                end = break_point + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Stop after last chunk
        if end >= text_length:
            break

        # Safe next position
        start = max(end - overlap, start + 1)

    return chunks


def split_by_sections(text: str) -> dict:
    section_headers = [
        "abstract",
        "introduction",
        "related work",
        "background",
        "methodology",
        "methods",
        "experiments",
        "results",
        "discussion",
        "conclusion",
        "references"
    ]

    pattern = r'(?i)\b(' + '|'.join(section_headers) + r')\b'
    parts = re.split(pattern, text)

    sections = {}
    i = 0

    while i < len(parts):
        part = parts[i].strip().lower()

        if part in section_headers and i + 1 < len(parts):
            sections[part.title()] = parts[i + 1].strip()
            i += 2
        else:
            i += 1

    return sections