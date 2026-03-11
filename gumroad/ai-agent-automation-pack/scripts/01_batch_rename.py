"""
01_batch_rename.py — AI-powered batch file renaming
Renames files in a directory using patterns or AI-suggested names.

Usage:
    python 01_batch_rename.py --dir ./photos --pattern "photo_{n:04d}{ext}"
    python 01_batch_rename.py --dir ./docs --prefix "2026-03-11_"
"""
import os
import argparse
from pathlib import Path


def batch_rename(directory: str, pattern: str = None, prefix: str = "", suffix: str = "", dry_run: bool = True):
    """Rename files matching a pattern in a directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory not found: {directory}")

    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    renamed = []

    for n, file in enumerate(files, start=1):
        ext = file.suffix
        stem = file.stem

        if pattern:
            new_name = pattern.format(n=n, ext=ext, stem=stem, name=file.name)
        else:
            new_name = f"{prefix}{stem}{suffix}{ext}"

        new_path = dir_path / new_name

        if dry_run:
            print(f"  [DRY RUN] {file.name} → {new_name}")
        else:
            file.rename(new_path)
            print(f"  Renamed: {file.name} → {new_name}")

        renamed.append({"old": file.name, "new": new_name})

    return renamed


def main():
    parser = argparse.ArgumentParser(description="Batch rename files")
    parser.add_argument("--dir", required=True, help="Directory to process")
    parser.add_argument("--pattern", help="Name pattern, e.g. 'file_{n:04d}{ext}'")
    parser.add_argument("--prefix", default="", help="Add prefix to filenames")
    parser.add_argument("--suffix", default="", help="Add suffix before extension")
    parser.add_argument("--execute", action="store_true", help="Actually rename (default is dry run)")
    args = parser.parse_args()

    dry_run = not args.execute
    if dry_run:
        print("DRY RUN mode — use --execute to apply changes\n")

    results = batch_rename(args.dir, args.pattern, args.prefix, args.suffix, dry_run)
    print(f"\n{'Would rename' if dry_run else 'Renamed'} {len(results)} files.")


if __name__ == "__main__":
    main()
