from __future__ import annotations

import json
from pathlib import Path

import internetarchive


OUTPUT_FILE = Path("data/archive_metadata.json")
COLLECTION = "zarke1"


def select_original_file(files: list[dict]) -> dict | None:
    mp4s = [
        f for f in files
        if f.get("name", "").endswith(".mp4")
        and not f.get("name", "").endswith(".ia.mp4")
    ]

    if not mp4s:
        return None

    return mp4s[0]


def build_entry(item: dict) -> dict | None:
    metadata = item.get("metadata", {})
    files = item.get("files", [])

    original = select_original_file(files)

    if not original:
        return None

    return {
        "identifier": item["identifier"],
        "title": metadata.get("title", item["identifier"]),
        "mediatype": metadata.get("mediatype"),
        "addeddate": metadata.get("addeddate"),
        "description": metadata.get("description", ""),
        "archive_url": f"https://archive.org/details/{item['identifier']}",
        "download_url": (
            f"https://archive.org/download/"
            f"{item['identifier']}/{original['name']}"
        ),
        "filename": original["name"],
        "size": original.get("size"),
        "format": original.get("format"),
        "duration": original.get("length"),
        "width": original.get("width"),
        "height": original.get("height"),
    }


def main() -> None:
    search = internetarchive.search_items(
        f"collection:{COLLECTION}"
    )

    results = []

    for result in search:
        identifier = result["identifier"]

        item = internetarchive.get_item(identifier)

        entry = build_entry(item.item_metadata)

        if entry:
            results.append(entry)

            print(
                f"Added: {entry['identifier']} "
                f"({entry['width']}x{entry['height']})"
            )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved {len(results)} entries")


if __name__ == "__main__":
    main()
