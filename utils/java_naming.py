# utils/java_naming.py

import re

def to_camel_case(snake_str: str) -> str:
    parts = re.split(r'[^a-zA-Z0-9]', snake_str)
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:] if word)
