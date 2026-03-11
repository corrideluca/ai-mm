"""
06_log_parser.py — Parse and filter log files
Extract errors, warnings, and patterns from log files.

Usage:
    python 06_log_parser.py --file app.log --level ERROR
    python 06_log_parser.py --file app.log --pattern "timeout|connection refused" --last 100
    python 06_log_parser.py --file app.log --stats
"""
import re
import sys
import argparse
from pathlib import Path
from collections import Counter


# Common log patterns
LEVEL_PATTERN = re.compile(
    r"\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL|TRACE)\b", re.IGNORECASE
)
TIMESTAMP_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})"
)


def parse_log_line(line: str) -> dict:
    """Extract metadata from a log line."""
    level_match = LEVEL_PATTERN.search(line)
    ts_match = TIMESTAMP_PATTERN.search(line)
    return {
        "line": line.rstrip(),
        "level": level_match.group(1).upper() if level_match else "UNKNOWN",
        "timestamp": ts_match.group(1) if ts_match else None,
    }


def filter_logs(
    lines: list[str],
    level: str = None,
    pattern: str = None,
    last: int = None,
) -> list[dict]:
    """Filter log lines by level and/or pattern."""
    parsed = [parse_log_line(l) for l in lines if l.strip()]

    if level:
        target_levels = {level.upper()}
        # Include higher severity levels
        severity = ["DEBUG", "TRACE", "INFO", "WARNING", "WARN", "ERROR", "CRITICAL", "FATAL"]
        if level.upper() in severity:
            idx = severity.index(level.upper())
            target_levels = set(severity[idx:])
        parsed = [p for p in parsed if p["level"] in target_levels]

    if pattern:
        regex = re.compile(pattern, re.IGNORECASE)
        parsed = [p for p in parsed if regex.search(p["line"])]

    if last:
        parsed = parsed[-last:]

    return parsed


def print_stats(lines: list[str]):
    """Print statistics about log levels."""
    parsed = [parse_log_line(l) for l in lines if l.strip()]
    counts = Counter(p["level"] for p in parsed)
    total = len(parsed)

    print(f"Total lines: {total}\n")
    for level in ["FATAL", "CRITICAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "TRACE", "UNKNOWN"]:
        if counts[level]:
            pct = counts[level] / total * 100
            bar = "█" * int(pct / 2)
            print(f"  {level:10s} {counts[level]:6d}  ({pct:5.1f}%)  {bar}")


def main():
    parser = argparse.ArgumentParser(description="Parse and filter log files")
    parser.add_argument("--file", help="Log file path (or stdin)")
    parser.add_argument("--level", help="Minimum log level (DEBUG/INFO/WARNING/ERROR)")
    parser.add_argument("--pattern", help="Regex pattern to filter lines")
    parser.add_argument("--last", type=int, help="Show last N matching lines")
    parser.add_argument("--stats", action="store_true", help="Show level statistics")
    args = parser.parse_args()

    if args.file:
        lines = Path(args.file).read_text().splitlines()
    else:
        lines = sys.stdin.read().splitlines()

    if not lines:
        print("No input provided.")
        sys.exit(1)

    if args.stats:
        print_stats(lines)
        return

    results = filter_logs(lines, args.level, args.pattern, args.last)

    for r in results:
        print(r["line"])

    if not results:
        print(f"No matching lines found.")
    else:
        print(f"\n--- {len(results)} line(s) matched ---", file=sys.stderr)


if __name__ == "__main__":
    main()
