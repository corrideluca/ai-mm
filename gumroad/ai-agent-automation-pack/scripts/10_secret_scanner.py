"""
10_secret_scanner.py — Scan files for accidentally committed secrets
Detect API keys, tokens, passwords, and credentials in your codebase.

Usage:
    python 10_secret_scanner.py --dir .
    python 10_secret_scanner.py --dir ./src --extensions py,js,ts,env
    python 10_secret_scanner.py --file .env --report findings.json
"""
import re
import sys
import json
import argparse
from pathlib import Path


# Secret detection patterns (regex)
SECRET_PATTERNS = [
    ("AWS Access Key",        r"AKIA[0-9A-Z]{16}"),
    ("AWS Secret Key",        r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]"),
    ("GitHub Token",          r"ghp_[0-9a-zA-Z]{36}"),
    ("GitHub OAuth",          r"gho_[0-9a-zA-Z]{36}"),
    ("OpenAI API Key",        r"sk-[a-zA-Z0-9]{48}"),
    ("Anthropic API Key",     r"sk-ant-[a-zA-Z0-9\-]{50,}"),
    ("Generic API Key",       r"(?i)(api[_-]?key|apikey)\s*[=:]\s*['\"][a-zA-Z0-9\-_]{20,}['\"]"),
    ("Generic Secret",        r"(?i)(secret|password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{8,}['\"]"),
    ("Private Key Header",    r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ("Bearer Token",          r"(?i)bearer\s+[a-zA-Z0-9\-_\.]{20,}"),
    ("Slack Token",           r"xox[baprs]-[0-9a-zA-Z\-]{10,}"),
    ("Stripe Key",            r"(?:sk|pk)_(live|test)_[0-9a-zA-Z]{24,}"),
    ("Twilio Key",            r"SK[0-9a-fA-F]{32}"),
    ("Google API Key",        r"AIza[0-9A-Za-z\-_]{35}"),
    ("Postgres URL",          r"postgres://[^:]+:[^@]+@"),
    ("MongoDB URL",           r"mongodb(\+srv)?://[^:]+:[^@]+@"),
    ("Private IP",            r"(?:10|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\.\d+\.\d+"),
]

# Files/dirs to always skip
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
SKIP_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock"}


def scan_file(filepath: Path, patterns: list) -> list[dict]:
    """Scan a single file for secrets."""
    findings = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        for line_num, line in enumerate(lines, start=1):
            for name, pattern in patterns:
                if re.search(pattern, line):
                    # Redact the actual secret value
                    redacted = re.sub(pattern, "[REDACTED]", line).strip()
                    findings.append({
                        "file": str(filepath),
                        "line": line_num,
                        "type": name,
                        "preview": redacted[:120],
                    })
    except (OSError, PermissionError):
        pass
    return findings


def scan_directory(root: str, extensions: list[str] = None) -> list[dict]:
    """Scan all files in directory for secrets."""
    root_path = Path(root)
    all_findings = []

    for filepath in root_path.rglob("*"):
        if not filepath.is_file():
            continue
        if any(part in SKIP_DIRS for part in filepath.parts):
            continue
        if filepath.name in SKIP_FILES:
            continue
        if extensions and filepath.suffix.lstrip(".") not in extensions:
            continue

        findings = scan_file(filepath, SECRET_PATTERNS)
        all_findings.extend(findings)

    return all_findings


def main():
    parser = argparse.ArgumentParser(description="Scan for accidentally committed secrets")
    parser.add_argument("--dir", help="Directory to scan")
    parser.add_argument("--file", help="Single file to scan")
    parser.add_argument("--extensions", help="File extensions to scan, e.g. py,js,ts,env")
    parser.add_argument("--report", help="Save findings to JSON file")
    args = parser.parse_args()

    extensions = args.extensions.split(",") if args.extensions else None

    findings = []
    if args.file:
        findings = scan_file(Path(args.file), SECRET_PATTERNS)
    elif args.dir:
        print(f"Scanning {args.dir}...")
        findings = scan_directory(args.dir, extensions)
    else:
        print("Use --dir or --file")
        sys.exit(1)

    if findings:
        print(f"\n⚠  Found {len(findings)} potential secret(s):\n")
        for f in findings:
            print(f"  [{f['type']}] {f['file']}:{f['line']}")
            print(f"      {f['preview']}")
    else:
        print("\n✓ No secrets detected.")

    if args.report:
        Path(args.report).write_text(json.dumps(findings, indent=2))
        print(f"\nReport saved to {args.report}")

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
