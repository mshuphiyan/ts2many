# utils/file_utils.py

from pathlib import Path

def save_java_file(file_path: Path, code: str):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ Saved: {file_path}")
