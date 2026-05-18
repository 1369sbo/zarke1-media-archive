from __future__ import annotations

import json
from pathlib import Path


INPUT_FILE = Path("archive_metadata_chronological_reverse.json")
OUTPUT_DIR = Path("data/items2")


def sanitize_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        name = name.replace(char, "_")

    return name


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        entries = json.load(f)

    if not isinstance(entries, list):
        raise TypeError(
            "archive_metadata.json must contain a list"
        )

    written = 0

    for entry in entries:
        identifier = entry.get("identifier")

        if not identifier:
            print("Skipping entry with no identifier")
            continue

        filename = sanitize_filename(identifier)

        output_path = OUTPUT_DIR / f"{filename}.json"

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)

        written += 1

        print(f"Wrote {output_path.name}")

    print(f"\nDone. Wrote {written} files.")


if __name__ == "__main__":
    main()