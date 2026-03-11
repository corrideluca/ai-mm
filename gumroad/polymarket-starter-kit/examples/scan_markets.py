"""Scan for markets resolving soon. Feed output to Claude/GPT for analysis."""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from agents.researcher import scan_overnight, scan_markets

parser = argparse.ArgumentParser(description="Scan Polymarket for opportunities")
parser.add_argument("--hours", type=int, default=48, help="Hours ahead to look (default: 48)")
parser.add_argument("--all", action="store_true", help="Scan all markets, not just upcoming")
args = parser.parse_args()

print(f"\nScanning markets...")

if args.all:
    data = scan_markets(limit=50)
    print(f"Found {data['count']} active markets\n")
else:
    # Try progressively wider windows
    data = {"count": 0}
    for hours in [args.hours, 168, 504]:
        data = scan_overnight(hours=hours)
        if data["count"] > 0:
            break
    print(f"Found {data['count']} markets resolving in next {data.get('cutoff_hours', args.hours)}h\n")

# Print as JSON for AI analysis
print(json.dumps(data, indent=2))

print(f"\n--- How to use this ---")
print("Copy the JSON above and paste into Claude Code:")
print('"Which of these markets are mispriced? What should I bet and why?"')
