"""
09_git_summary.py — Git repository activity summarizer
Show recent commits, file changes, and contributor stats.

Usage:
    python 09_git_summary.py --days 7
    python 09_git_summary.py --days 30 --author "Alex"
    python 09_git_summary.py --since 2026-03-01
"""
import sys
import argparse
import subprocess
from datetime import datetime, timedelta
from collections import Counter, defaultdict


def run_git(args: list[str], cwd: str = ".") -> str:
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        return ""


def get_commits(since: str = None, author: str = None) -> list[dict]:
    """Get list of commits with metadata."""
    cmd = ["log", "--format=%H|%an|%ae|%ai|%s", "--no-merges"]
    if since:
        cmd += [f"--since={since}"]
    if author:
        cmd += [f"--author={author}"]

    output = run_git(cmd)
    if not output:
        return []

    commits = []
    for line in output.splitlines():
        parts = line.split("|", 4)
        if len(parts) == 5:
            commits.append({
                "hash": parts[0][:8],
                "author": parts[1],
                "email": parts[2],
                "date": parts[3][:10],
                "message": parts[4],
            })
    return commits


def get_changed_files(since: str = None) -> Counter:
    """Count how many times each file was changed."""
    cmd = ["log", "--name-only", "--format=", "--no-merges"]
    if since:
        cmd += [f"--since={since}"]

    output = run_git(cmd)
    files = [l for l in output.splitlines() if l.strip()]
    return Counter(files)


def main():
    parser = argparse.ArgumentParser(description="Summarize git repository activity")
    parser.add_argument("--days", type=int, default=7, help="Analyze last N days")
    parser.add_argument("--since", help="Start date YYYY-MM-DD")
    parser.add_argument("--author", help="Filter by author name")
    parser.add_argument("--top-files", type=int, default=10, help="Show top N changed files")
    args = parser.parse_args()

    # Check if we're in a git repo
    if not run_git(["rev-parse", "--git-dir"]):
        print("Not a git repository.")
        sys.exit(1)

    since = args.since
    if not since:
        since = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    branch = run_git(["branch", "--show-current"])
    repo_name = run_git(["rev-parse", "--show-toplevel"])

    print(f"Git Summary: {repo_name.split('/')[-1] if repo_name else '.'}")
    print(f"Branch: {branch or 'unknown'}")
    print(f"Period: {since} → today")
    if args.author:
        print(f"Author: {args.author}")
    print(f"{'─' * 50}\n")

    commits = get_commits(since, args.author)

    if not commits:
        print("No commits found in this period.")
        return

    # Author stats
    author_counts = Counter(c["author"] for c in commits)
    print(f"Commits: {len(commits)}")
    print("\nTop contributors:")
    for author, count in author_counts.most_common(5):
        bar = "█" * min(count, 20)
        print(f"  {author:25s} {count:4d}  {bar}")

    # Daily activity
    daily = Counter(c["date"] for c in commits)
    print(f"\nDaily activity (last 7 days):")
    for date in sorted(daily.keys())[-7:]:
        count = daily[date]
        bar = "█" * count
        print(f"  {date}  {count:3d}  {bar}")

    # Recent commits
    print(f"\nRecent commits:")
    for c in commits[:10]:
        print(f"  {c['hash']}  {c['date']}  {c['author'][:15]:<15}  {c['message'][:60]}")

    # Most changed files
    changed_files = get_changed_files(since)
    if changed_files:
        print(f"\nTop {args.top_files} most changed files:")
        for filepath, count in changed_files.most_common(args.top_files):
            print(f"  {count:4d}x  {filepath}")


if __name__ == "__main__":
    main()
