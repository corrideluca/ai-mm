"""Risk manager — enforces percentage-based limits and tracks P&L."""

import json
from datetime import date
from pathlib import Path
from core.config import config

PERFORMANCE_FILE = Path(__file__).parent.parent / "memory" / "performance.md"


def check_can_trade(amount: float, balance: float) -> dict:
    """Check if a trade is allowed under risk limits. All limits are % based."""
    limits = config.risk
    reasons = []

    if balance <= 0:
        reasons.append("Balance is $0 — fund the wallet first")
        return {"allowed": False, "reasons": reasons, "balance": balance, "daily_pnl": 0, "amount": amount}

    max_bet = balance * limits.max_bet_pct
    if amount > max_bet:
        reasons.append(f"Bet ${amount:.2f} exceeds {limits.max_bet_pct*100:.0f}% of balance (max ${max_bet:.2f})")

    max_position = balance * limits.max_position_pct
    if amount > max_position:
        reasons.append(f"Bet ${amount:.2f} exceeds {limits.max_position_pct*100:.0f}% position limit (max ${max_position:.2f})")

    daily_loss = get_daily_pnl()
    max_daily_loss = balance * limits.daily_loss_pct
    if daily_loss < -max_daily_loss:
        reasons.append(f"Daily loss ${daily_loss:.2f} exceeds {limits.daily_loss_pct*100:.0f}% limit (max -${max_daily_loss:.2f})")

    return {
        "allowed": len(reasons) == 0,
        "reasons": reasons,
        "balance": balance,
        "max_bet": balance * limits.max_bet_pct,
        "daily_pnl": daily_loss,
        "amount": amount,
    }


def log_trade(trade: dict) -> None:
    """Log a trade to performance.md."""
    PERFORMANCE_FILE.parent.mkdir(exist_ok=True)

    entry = (
        f"\n| {date.today()} "
        f"| {trade.get('market', 'N/A')} "
        f"| {trade.get('side', 'N/A')} "
        f"| ${trade.get('amount', 0):.2f} "
        f"| {trade.get('price', 0):.2f} "
        f"| {trade.get('status', 'N/A')} "
        f"| {trade.get('reasoning', '')} |"
    )

    if not PERFORMANCE_FILE.exists():
        header = """# Trade Performance Log

| Date | Market | Side | Amount | Price | Status | Reasoning |
|------|--------|------|--------|-------|--------|-----------|"""
        PERFORMANCE_FILE.write_text(header + entry)
    else:
        with open(PERFORMANCE_FILE, "a") as f:
            f.write(entry)


def get_daily_pnl() -> float:
    """Calculate today's P&L from the log."""
    if not PERFORMANCE_FILE.exists():
        return 0.0

    today = str(date.today())
    total = 0.0
    for line in PERFORMANCE_FILE.read_text().splitlines():
        if line.startswith(f"| {today}") and "FILLED" in line:
            parts = [p.strip() for p in line.split("|")]
            try:
                amount = float(parts[4].replace("$", ""))
                side = parts[3]
                total -= amount if side == "BUY" else -amount
            except (ValueError, IndexError):
                continue
    return total
