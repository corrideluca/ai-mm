"""Polymarket Agent — CLI entry point. Autonomous mode — no confirmations."""

import argparse
import json
from rich.console import Console
from rich.table import Table

console = Console()


def cmd_scan(args):
    from agents.researcher import scan_markets
    console.print("[bold]Scanning markets...[/bold]")
    result = scan_markets(limit=args.limit)
    print(json.dumps(result, indent=2))


def cmd_status(args):
    from agents.trader import get_portfolio
    portfolio = get_portfolio()
    console.print(f"\n[bold]Balance:[/bold] ${portfolio['balance']:.2f}")
    console.print(f"[bold]Positions:[/bold] {len(portfolio['positions'])}")
    for pos in portfolio["positions"]:
        console.print(f"  • {pos}")


def cmd_bet(args):
    from agents.trader import execute_trade

    result = execute_trade(
        token_id=args.token_id,
        amount=args.amount,
        side=args.side,
        market_name=args.market or "",
        reasoning=args.reason or "autonomous trade",
    )
    print(json.dumps(result, indent=2))


def cmd_pnl(args):
    from agents.risk import get_daily_pnl
    from pathlib import Path

    perf_file = Path("memory/performance.md")
    if perf_file.exists():
        console.print(perf_file.read_text())
    console.print(f"\n[bold]Today's P&L:[/bold] ${get_daily_pnl():.2f}")


def cmd_detail(args):
    from agents.researcher import get_market_detail
    result = get_market_detail(args.condition_id)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Polymarket Agent")
    sub = parser.add_subparsers()

    p_scan = sub.add_parser("scan")
    p_scan.add_argument("--limit", type=int, default=20)
    p_scan.set_defaults(func=cmd_scan)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    p_bet = sub.add_parser("bet")
    p_bet.add_argument("token_id")
    p_bet.add_argument("amount", type=float)
    p_bet.add_argument("--side", default="BUY", choices=["BUY", "SELL"])
    p_bet.add_argument("--market", default="")
    p_bet.add_argument("--reason", default="")
    p_bet.set_defaults(func=cmd_bet)

    p_pnl = sub.add_parser("pnl")
    p_pnl.set_defaults(func=cmd_pnl)

    p_detail = sub.add_parser("detail")
    p_detail.add_argument("condition_id")
    p_detail.set_defaults(func=cmd_detail)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
