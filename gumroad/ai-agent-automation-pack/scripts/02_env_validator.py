"""
02_env_validator.py — Validate environment variables from .env files
Checks that all required env vars are present and non-empty.

Usage:
    python 02_env_validator.py --env .env --required OPENAI_API_KEY,DATABASE_URL
    python 02_env_validator.py --env .env.production --strict
"""
import os
import sys
import argparse
from pathlib import Path


def parse_env_file(filepath: str) -> dict:
    """Parse a .env file into a dict."""
    env = {}
    path = Path(filepath)
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def validate_env(env_file: str, required: list[str] = None, strict: bool = False) -> dict:
    """Validate env vars. Returns dict with 'passed', 'missing', 'empty', 'warnings'."""
    env = parse_env_file(env_file)

    # Also check actual process env
    full_env = {**env, **{k: v for k, v in os.environ.items() if k in (required or [])}}

    missing = []
    empty = []
    present = []

    for key in (required or list(env.keys())):
        val = full_env.get(key)
        if val is None:
            missing.append(key)
        elif val == "":
            empty.append(key)
        else:
            present.append(key)

    warnings = []
    if strict:
        for key, val in env.items():
            if "password" in key.lower() or "secret" in key.lower() or "key" in key.lower():
                if len(val) < 20:
                    warnings.append(f"{key}: looks too short for a secret")

    return {
        "passed": len(missing) == 0 and len(empty) == 0,
        "present": present,
        "missing": missing,
        "empty": empty,
        "warnings": warnings,
        "total": len(present) + len(missing) + len(empty),
    }


def main():
    parser = argparse.ArgumentParser(description="Validate environment variables")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    parser.add_argument("--required", help="Comma-separated list of required keys")
    parser.add_argument("--strict", action="store_true", help="Check for weak secrets")
    args = parser.parse_args()

    required = args.required.split(",") if args.required else None
    result = validate_env(args.env, required, args.strict)

    print(f"Validating: {args.env}")
    print(f"Total vars: {result['total']}\n")

    if result["present"]:
        print(f"  ✓ Present ({len(result['present'])}): {', '.join(result['present'])}")
    if result["missing"]:
        print(f"  ✗ MISSING ({len(result['missing'])}): {', '.join(result['missing'])}")
    if result["empty"]:
        print(f"  ⚠ EMPTY ({len(result['empty'])}): {', '.join(result['empty'])}")
    if result["warnings"]:
        print("\n  Warnings:")
        for w in result["warnings"]:
            print(f"    ⚠ {w}")

    print(f"\n{'✓ PASSED' if result['passed'] else '✗ FAILED'}")
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
