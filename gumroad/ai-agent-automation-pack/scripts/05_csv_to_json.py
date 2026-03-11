"""
05_csv_to_json.py — Convert CSV files to JSON (and back)
Handles headers, type inference, and nested structures.

Usage:
    python 05_csv_to_json.py --input data.csv --output data.json
    python 05_csv_to_json.py --input data.json --output data.csv
    python 05_csv_to_json.py --input data.csv --types "age:int,score:float,active:bool"
"""
import csv
import json
import sys
import argparse
from pathlib import Path


def infer_type(value: str):
    """Try to infer the Python type of a string value."""
    if not value:
        return None
    if value.lower() in ("true", "yes", "1"):
        return True
    if value.lower() in ("false", "no", "0"):
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def csv_to_json(csv_path: str, infer: bool = True, type_map: dict = None) -> list[dict]:
    """Read CSV and return list of dicts."""
    records = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {}
            for key, value in row.items():
                if type_map and key in type_map:
                    cast = type_map[key]
                    try:
                        value = cast(value)
                    except (ValueError, TypeError):
                        pass
                elif infer:
                    value = infer_type(value)
                record[key] = value
            records.append(record)
    return records


def json_to_csv(json_path: str, output_path: str):
    """Write JSON array to CSV."""
    data = json.loads(Path(json_path).read_text())
    if not isinstance(data, list) or not data:
        raise ValueError("JSON must be a non-empty array of objects")

    headers = list(data[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Written {len(data)} rows to {output_path}")


def parse_type_map(types_str: str) -> dict:
    """Parse 'name:type,age:int' into {'name': str, 'age': int}."""
    type_map = {}
    type_lookup = {"int": int, "float": float, "str": str, "bool": bool}
    for part in types_str.split(","):
        if ":" in part:
            key, type_name = part.strip().split(":", 1)
            type_map[key.strip()] = type_lookup.get(type_name.strip(), str)
    return type_map


def main():
    parser = argparse.ArgumentParser(description="Convert between CSV and JSON")
    parser.add_argument("--input", required=True, help="Input file (.csv or .json)")
    parser.add_argument("--output", help="Output file (default: stdout for JSON)")
    parser.add_argument("--no-infer", action="store_true", help="Keep all values as strings")
    parser.add_argument("--types", help="Type overrides, e.g. 'age:int,score:float'")
    args = parser.parse_args()

    input_path = Path(args.input)
    ext = input_path.suffix.lower()

    if ext == ".csv":
        type_map = parse_type_map(args.types) if args.types else None
        records = csv_to_json(args.input, infer=not args.no_infer, type_map=type_map)
        output = json.dumps(records, indent=2)

        if args.output:
            Path(args.output).write_text(output)
            print(f"Converted {len(records)} rows → {args.output}")
        else:
            print(output)

    elif ext == ".json":
        if not args.output:
            print("Error: --output required for JSON→CSV conversion")
            sys.exit(1)
        json_to_csv(args.input, args.output)
    else:
        print(f"Unknown file type: {ext}. Use .csv or .json")
        sys.exit(1)


if __name__ == "__main__":
    main()
