"""
07_dir_stats.py — Directory statistics and disk usage analyzer
Show file counts, sizes, and distribution by type in a directory.

Usage:
    python 07_dir_stats.py --dir ./src
    python 07_dir_stats.py --dir . --top 20 --exclude .git,node_modules
"""
import os
import argparse
from pathlib import Path
from collections import defaultdict


def format_size(bytes_: int) -> str:
    """Human-readable file size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"


def analyze_directory(root: str, exclude: list[str] = None) -> dict:
    """Recursively analyze directory contents."""
    exclude = set(exclude or [])
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "by_extension": defaultdict(lambda: {"count": 0, "size": 0}),
        "largest_files": [],
        "empty_files": 0,
    }

    root_path = Path(root)

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip excluded dirs
        dirnames[:] = [d for d in dirnames if d not in exclude]

        stats["total_dirs"] += 1

        for filename in filenames:
            filepath = Path(dirpath) / filename
            try:
                size = filepath.stat().st_size
            except (OSError, PermissionError):
                continue

            stats["total_files"] += 1
            stats["total_size"] += size

            ext = filepath.suffix.lower() or "(no ext)"
            stats["by_extension"][ext]["count"] += 1
            stats["by_extension"][ext]["size"] += size

            if size == 0:
                stats["empty_files"] += 1

            stats["largest_files"].append((size, str(filepath.relative_to(root_path))))

    stats["largest_files"].sort(reverse=True)
    stats["largest_files"] = stats["largest_files"][:20]

    return stats


def main():
    parser = argparse.ArgumentParser(description="Analyze directory statistics")
    parser.add_argument("--dir", default=".", help="Directory to analyze")
    parser.add_argument("--top", type=int, default=10, help="Show top N file types")
    parser.add_argument("--largest", type=int, default=5, help="Show N largest files")
    parser.add_argument("--exclude", help="Comma-separated dirs to exclude (e.g. .git,node_modules)")
    args = parser.parse_args()

    exclude = args.exclude.split(",") if args.exclude else []
    stats = analyze_directory(args.dir, exclude)

    print(f"Directory: {args.dir}")
    print(f"{'─' * 50}")
    print(f"  Files:      {stats['total_files']:,}")
    print(f"  Dirs:       {stats['total_dirs']:,}")
    print(f"  Total size: {format_size(stats['total_size'])}")
    print(f"  Empty files:{stats['empty_files']}")

    print(f"\nTop {args.top} file types by count:")
    by_ext = sorted(stats["by_extension"].items(), key=lambda x: x[1]["count"], reverse=True)
    for ext, info in by_ext[:args.top]:
        bar = "█" * min(int(info["count"] / max(by_ext[0][1]["count"], 1) * 20), 20)
        print(f"  {ext:15s} {info['count']:6,} files  {format_size(info['size']):>10}  {bar}")

    if stats["largest_files"]:
        print(f"\nLargest {args.largest} files:")
        for size, path in stats["largest_files"][:args.largest]:
            print(f"  {format_size(size):>10}  {path}")


if __name__ == "__main__":
    main()
