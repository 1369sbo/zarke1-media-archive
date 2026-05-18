from __future__ import annotations

import json
from pathlib import Path

import internetarchive as ia


OUTPUT_FILE = Path("data/archive_metadata.json")

SEARCH_QUERY = "uploader:@gmail.com"


def select_original_file(files: list[dict]) -> dict | None:
    candidates = []

    for f in files:
        name = f.get("name", "")

        if not name.endswith(".mp4"):
            continue

        if name.endswith(".ia.mp4"):
            continue

        candidates.append(f)

    if not candidates:
        return None

    return candidates[0]


def build_entry(identifier: str) -> dict | None:
    item = ia.get_item(identifier)

    metadata = item.metadata
    files = item.files

    original = select_original_file(files)

    if not original:
        print(f"Skipping {identifier} (no original mp4)")
        return None

    width = original.get("width")
    height = original.get("height")

    resolution = None

    if width and height:
        resolution = f"{width}x{height}"

    return {
        "identifier": identifier,
        "title": metadata.get("title", identifier),
        "addeddate": metadata.get("addeddate"),
        "description": metadata.get("description", ""),
        "archive_url": (
            f"https://archive.org/details/{identifier}"
        ),
        "download_url": (
            f"https://archive.org/download/"
            f"{identifier}/{original['name']}"
        ),
        "filename": original.get("name"),
        "format": original.get("format"),
        "size": original.get("size"),
        "duration": original.get("length"),
        "width": width,
        "height": height,
        "resolution": resolution,
    }


def main() -> None:
    results = []

    search = ia.search_items(SEARCH_QUERY)

    for i, result in enumerate(search):
        identifier = result["identifier"]

        print(f"[{i}] Fetching {identifier}")

        try:
            entry = build_entry(identifier)

            if entry:
                results.append(entry)

        except Exception as exc:
            print(f"ERROR: {identifier}")
            print(exc)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved {len(results)} entries")


if __name__ == "__main__":
    main()
