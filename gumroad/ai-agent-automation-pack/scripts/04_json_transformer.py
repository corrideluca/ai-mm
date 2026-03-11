"""
04_json_transformer.py — Transform JSON files with jq-style queries
Filter, map, and reshape JSON data from files or stdin.

Usage:
    python 04_json_transformer.py --file data.json --select "name,email"
    python 04_json_transformer.py --file data.json --filter "age>18" --output filtered.json
    echo '[{"name":"Alice","age":30}]' | python 04_json_transformer.py --select "name"
"""
import sys
import json
import argparse
from pathlib import Path


def select_fields(data: list | dict, fields: list[str]) -> list | dict:
    """Keep only specified fields from objects."""
    if isinstance(data, list):
        return [{f: item.get(f) for f in fields if f in item} for item in data]
    elif isinstance(data, dict):
        return {f: data.get(f) for f in fields if f in data}
    return data


def filter_records(data: list, condition: str) -> list:
    """Filter list by simple condition like 'age>18' or 'active==true'."""
    if not isinstance(data, list):
        return data

    results = []
    for item in data:
        try:
            if evaluate_condition(item, condition):
                results.append(item)
        except Exception:
            pass
    return results


def evaluate_condition(item: dict, condition: str) -> bool:
    """Evaluate a simple filter condition against a dict."""
    for op in [">=", "<=", "!=", "==", ">", "<"]:
        if op in condition:
            key, value = condition.split(op, 1)
            key = key.strip()
            value = value.strip()

            item_val = item.get(key)
            if item_val is None:
                return False

            # Type coerce
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.isdigit():
                value = int(value)
                item_val = int(item_val) if str(item_val).isdigit() else item_val
            else:
                try:
                    value = float(value)
                    item_val = float(item_val)
                except (ValueError, TypeError):
                    pass

            ops = {">=": lambda a, b: a >= b, "<=": lambda a, b: a <= b,
                   "!=": lambda a, b: a != b, "==": lambda a, b: a == b,
                   ">": lambda a, b: a > b, "<": lambda a, b: a < b}
            return ops[op](item_val, value)

    return False


def main():
    parser = argparse.ArgumentParser(description="Transform JSON data")
    parser.add_argument("--file", help="Input JSON file (or pipe via stdin)")
    parser.add_argument("--select", help="Comma-separated fields to keep")
    parser.add_argument("--filter", dest="filter_cond", help="Filter condition, e.g. 'age>18'")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--pretty", action="store_true", default=True, help="Pretty print output")
    args = parser.parse_args()

    # Load data
    if args.file:
        data = json.loads(Path(args.file).read_text())
    else:
        data = json.loads(sys.stdin.read())

    # Apply transformations
    if args.filter_cond and isinstance(data, list):
        data = filter_records(data, args.filter_cond)
        print(f"Filter applied: {len(data)} records matched", file=sys.stderr)

    if args.select:
        fields = [f.strip() for f in args.select.split(",")]
        data = select_fields(data, fields)

    # Output
    indent = 2 if args.pretty else None
    output = json.dumps(data, indent=indent)

    if args.output:
        Path(args.output).write_text(output)
        count = len(data) if isinstance(data, list) else 1
        print(f"Written {count} record(s) to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
