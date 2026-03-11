"""
03_api_health_check.py — HTTP endpoint health checker
Check if a list of API endpoints are alive and responding correctly.

Usage:
    python 03_api_health_check.py --urls http://localhost:3000/health,https://api.example.com/ping
    python 03_api_health_check.py --file endpoints.txt --timeout 5
"""
import sys
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path


def check_endpoint(url: str, timeout: int = 10, expected_status: int = 200) -> dict:
    """Check a single HTTP endpoint. Returns result dict."""
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "health-checker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = (time.time() - start) * 1000
            status = resp.status
            return {
                "url": url,
                "status": status,
                "ok": status == expected_status,
                "latency_ms": round(elapsed, 1),
                "error": None,
            }
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        return {
            "url": url,
            "status": e.code,
            "ok": e.code == expected_status,
            "latency_ms": round(elapsed, 1),
            "error": str(e),
        }
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        return {
            "url": url,
            "status": None,
            "ok": False,
            "latency_ms": round(elapsed, 1),
            "error": str(e),
        }


def check_all(urls: list[str], timeout: int = 10, expected_status: int = 200) -> list[dict]:
    results = []
    for url in urls:
        result = check_endpoint(url, timeout, expected_status)
        icon = "✓" if result["ok"] else "✗"
        status = result["status"] or "ERR"
        latency = result["latency_ms"]
        print(f"  {icon} [{status}] {url} ({latency}ms)")
        if result["error"] and not result["ok"]:
            print(f"      Error: {result['error']}")
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description="Check HTTP endpoint health")
    parser.add_argument("--urls", help="Comma-separated list of URLs")
    parser.add_argument("--file", help="File with one URL per line")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--expected", type=int, default=200, help="Expected HTTP status code")
    args = parser.parse_args()

    urls = []
    if args.urls:
        urls.extend([u.strip() for u in args.urls.split(",")])
    if args.file:
        path = Path(args.file)
        if path.exists():
            urls.extend([l.strip() for l in path.read_text().splitlines() if l.strip()])

    if not urls:
        print("No URLs provided. Use --urls or --file.")
        sys.exit(1)

    print(f"Checking {len(urls)} endpoint(s)...\n")
    results = check_all(urls, args.timeout, args.expected)

    passed = sum(1 for r in results if r["ok"])
    failed = len(results) - passed

    print(f"\nResults: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
