#!/usr/bin/env python3
"""
Sort archive metadata JSON file by date and title.

This script reads archive_metadata.json and creates two new sorted copies:
1. archive_metadata_chronological_reverse.json - sorted by addeddate (newest first)
2. archive_metadata_alphabetical.json - sorted by title (A-Z)

Usage:
    python sort_metadata.py
"""

import json
from datetime import datetime
from pathlib import Path


def load_metadata(file_path):
    """Load metadata from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_metadata(data, file_path):
    """Save metadata to JSON file with proper formatting."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved: {file_path}")


def sort_by_date_reverse(data):
    """Sort entries by addeddate in reverse chronological order (newest first)."""
    def parse_date(entry):
        try:
            return datetime.strptime(entry.get('addeddate', ''), '%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            return datetime.min
    
    return sorted(data, key=parse_date, reverse=True)


def sort_by_title_alpha(data):
    """Sort entries by title in alphabetical order (A-Z)."""
    return sorted(data, key=lambda x: x.get('title', '').lower())


def main():
    script_dir = Path(__file__).parent
    metadata_file = script_dir / 'archive_metadata.json'
    
    if not metadata_file.exists():
        print(f"Error: {metadata_file} not found!")
        return
    
    print(f"Loading metadata from {metadata_file}...")
    metadata = load_metadata(metadata_file)
    print(f"Loaded {len(metadata)} entries")
    
    # Sort by date (reverse chronological)
    print("\nSorting by date (newest first)...")
    chronological = sort_by_date_reverse(metadata)
    chrono_file = script_dir / 'archive_metadata_chronological_reverse.json'
    save_metadata(chronological, chrono_file)
    
    # Sort by title (alphabetical)
    print("Sorting by title (A-Z)...")
    alphabetical = sort_by_title_alpha(metadata)
    alpha_file = script_dir / 'archive_metadata_alphabetical.json'
    save_metadata(alphabetical, alpha_file)
    
    print("\n✓ Done! Created:")
    print(f"  - {chrono_file.name}")
    print(f"  - {alpha_file.name}")


if __name__ == '__main__':
    main()
