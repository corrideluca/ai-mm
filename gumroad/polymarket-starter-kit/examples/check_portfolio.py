"""Check your portfolio: balance, open orders, positions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.trader import get_portfolio

portfolio = get_portfolio()

print(f"\n=== Portfolio ===")
print(f"Balance: ${portfolio['balance']:.2f} USDC")

orders = portfolio.get("orders", [])
print(f"Open orders: {len(orders) if isinstance(orders, list) else 'N/A'}")
for o in (orders if isinstance(orders, list) else []):
    print(f"  - {o}")

positions = portfolio.get("positions", [])
print(f"Positions: {len(positions) if isinstance(positions, list) else 'N/A'}")
for p in (positions if isinstance(positions, list) else []):
    print(f"  - {p}")
