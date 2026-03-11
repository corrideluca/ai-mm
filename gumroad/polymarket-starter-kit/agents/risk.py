"""Risk manager — enforces % -based limits and logs every trade.

All limits are percentage-based so they automatically scale
with your balance. No hardcoded dollar amounts.
"""

from datetime import date
from pathlib import Path
from core.config import config

TRADE_LOG = Path("memory/performance.md")


def check_can_trade(amount: float, balance: float) -> dict:
    """Check if a trade passes all risk limits.

    Returns:
        {
            "allowed": bool,
            "reasons": list[str],  # why it was blocked (empty if allowed)
            "balance": float,
            "max_bet": float,
            "daily_pnl": float,
        }
    """
    limits = config.risk
    reasons = []

    if balance <= 0:
        return {
            "allowed": False,
            "reasons": ["Balance is $0 — fund your wallet first"],
            "balance": balance,
            "daily_pnl": 0,
            "amount": amount,
        }

    max_bet = balance * limits.max_bet_pct
    if amount > max_bet:
        reasons.append(
            f"${amount:.2f} exceeds max single bet "
            f"({limits.max_bet_pct*100:.0f}% of balance = ${max_bet:.2f})"
        )

    daily_loss = get_daily_pnl()
    max_daily_loss = balance * limits.daily_loss_pct
    if daily_loss < -max_daily_loss:
        reasons.append(
            f"Daily loss ${daily_loss:.2f} exceeds "
            f"{limits.daily_loss_pct*100:.0f}% limit (${max_daily_loss:.2f})"
        )

    return {
        "allowed": len(reasons) == 0,
        "reasons": reasons,
        "balance": balance,
        "max_bet": max_bet,
        "daily_pnl": daily_loss,
        "amount": amount,
    }


def log_trade(trade: dict) -> None:
    """Append a trade to the performance log (markdown table)."""
    TRADE_LOG.parent.mkdir(exist_ok=True)

    row = (
        f"\n| {date.today()} "
        f"| {trade.get('market', 'N/A')} "
        f"| {trade.get('side', 'N/A')} "
        f"| ${trade.get('amount', 0):.2f} "
        f"| {trade.get('price', 0):.2f} "
        f"| {trade.get('status', 'N/A')} "
        f"| {trade.get('reasoning', '')} |"
    )

    if not TRADE_LOG.exists():
        TRADE_LOG.write_text(
            "# Trade Log\n\n"
            "| Date | Market | Side | Amount | Price | Status | Reasoning |\n"
            "|------|--------|------|--------|-------|--------|-----------|"
            + row
        )
    else:
        with open(TRADE_LOG, "a") as f:
            f.write(row)


def get_daily_pnl() -> float:
    """Calculate today's realized P&L from the trade log.

    Returns negative number if net loss (e.g., -3.50 = lost $3.50 today).
    """
    if not TRADE_LOG.exists():
        return 0.0

    today = str(date.today())
    total = 0.0

    for line in TRADE_LOG.read_text().splitlines():
        if not line.startswith(f"| {today}"):
            continue
        if "FILLED" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        try:
            amount = float(parts[4].replace("$", ""))
            side = parts[3]
            total -= amount if side == "BUY" else -amount
        except (ValueError, IndexError):
            continue

    return total
