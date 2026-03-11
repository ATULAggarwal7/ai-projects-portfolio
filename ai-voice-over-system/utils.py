# utils.py
import re
import json


# Reuse preserve-case replacement logic
def replace_preserve_case(match, replacement):
    orig = match.group(0)
    safe_replacement = replacement.strip()
    if orig.isupper():
        return safe_replacement.upper()
    if orig.istitle():
        return (
            safe_replacement[0].upper() + safe_replacement[1:]
            if safe_replacement
            else safe_replacement
        )
    return safe_replacement


def apply_dictionary(text, custom_dict):
    if not custom_dict:
        return text

    # sort keys longest → shortest to avoid partial replacements
    keys = sorted(custom_dict.keys(), key=len, reverse=True)
    new_text = text

    for key in keys:
        correction = custom_dict[key]
        correction = correction.replace("ː", "").replace("ˈ", "")

        if re.match(r"^[\w\s]+$", key):
            pattern = r"\b" + re.escape(key) + r"\b"
        else:
            pattern = re.escape(key)

        new_text = re.sub(
            pattern,
            lambda m: replace_preserve_case(m, correction),
            new_text,
            flags=re.IGNORECASE,
        )

    return new_text


def split_text_into_chunks(text, max_len=250):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks = []

    for sentence in sentences:
        words = sentence.split()
        current = ""
        for word in words:
            if len(current) + len(word) + 1 <= max_len:
                current += (" " if current else "") + word
            else:
                chunks.append(current)
                current = word
        if current:
            chunks.append(current)

    return [c.strip() for c in chunks if c.strip()]
