"""
08_port_scanner.py — Local port scanner for development
Check which ports are open on localhost for debugging your dev stack.

Usage:
    python 08_port_scanner.py --host localhost --ports 3000,8080,5432,6379
    python 08_port_scanner.py --host localhost --range 3000-3010
    python 08_port_scanner.py --common  # Scan common dev ports
"""
import sys
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


# Common development ports
COMMON_PORTS = {
    3000: "Next.js/React dev server",
    3001: "Create React App",
    4000: "Gatsby/Phoenix",
    5000: "Flask/Python dev",
    5432: "PostgreSQL",
    5433: "PostgreSQL (alt)",
    6379: "Redis",
    6380: "Redis (alt)",
    7700: "MeiliSearch",
    8000: "Django/FastAPI/Uvicorn",
    8080: "Spring/Generic HTTP",
    8443: "HTTPS alt",
    8888: "Jupyter Notebook",
    9000: "SonarQube/PHP-FPM",
    9200: "Elasticsearch",
    9090: "Prometheus",
    27017: "MongoDB",
    27018: "MongoDB (alt)",
}


def check_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Return True if port is open."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def scan_ports(host: str, ports: list[int], timeout: float = 0.5) -> list[dict]:
    """Scan multiple ports concurrently."""
    results = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_port = {
            executor.submit(check_port, host, port, timeout): port
            for port in ports
        }
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            is_open = future.result()
            results.append({
                "port": port,
                "open": is_open,
                "service": COMMON_PORTS.get(port, ""),
            })

    results.sort(key=lambda x: x["port"])
    return results


def main():
    parser = argparse.ArgumentParser(description="Scan local ports for dev debugging")
    parser.add_argument("--host", default="localhost", help="Host to scan")
    parser.add_argument("--ports", help="Comma-separated ports, e.g. 3000,8080,5432")
    parser.add_argument("--range", dest="port_range", help="Port range, e.g. 3000-3010")
    parser.add_argument("--common", action="store_true", help="Scan common dev ports")
    parser.add_argument("--timeout", type=float, default=0.5, help="Timeout per port in seconds")
    parser.add_argument("--open-only", action="store_true", help="Only show open ports")
    args = parser.parse_args()

    ports = []
    if args.common:
        ports = list(COMMON_PORTS.keys())
    if args.ports:
        ports.extend([int(p.strip()) for p in args.ports.split(",") if p.strip().isdigit()])
    if args.port_range:
        start, end = args.port_range.split("-")
        ports.extend(range(int(start), int(end) + 1))

    if not ports:
        print("No ports specified. Use --ports, --range, or --common")
        sys.exit(1)

    ports = sorted(set(ports))
    print(f"Scanning {args.host} ({len(ports)} ports)...\n")

    results = scan_ports(args.host, ports, args.timeout)
    open_count = sum(1 for r in results if r["open"])

    for r in results:
        if args.open_only and not r["open"]:
            continue
        status = "OPEN  ✓" if r["open"] else "closed"
        service = f"  ({r['service']})" if r["service"] else ""
        print(f"  :{r['port']:<6} {status}{service}")

    print(f"\n{open_count} port(s) open out of {len(ports)} scanned.")


if __name__ == "__main__":
    main()
