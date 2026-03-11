"""Place a single trade from the command line.

Usage:
    python place_trade.py --token-id 0x123... --amount 5 --side BUY
    python place_trade.py --token-id 0x123... --amount 10 --side BUY --reason "Strong edge"
"""

import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.trader import execute_trade

parser = argparse.ArgumentParser(description="Place a Polymarket trade")
parser.add_argument("--token-id", required=True, help="Token ID from market data")
parser.add_argument("--amount", type=float, required=True, help="USDC amount (e.g. 5.00)")
parser.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
parser.add_argument("--market", default="", help="Market name for logging")
parser.add_argument("--reason", default="", help="Why you're making this trade")
parser.add_argument("--price", type=float, default=None, help="Override price (fetches live if not set)")
args = parser.parse_args()

print(f"\nPlacing trade...")
print(f"  Token: {args.token_id}")
print(f"  Amount: ${args.amount:.2f}")
print(f"  Side: {args.side}")

result = execute_trade(
    token_id=args.token_id,
    amount=args.amount,
    side=args.side,
    market_name=args.market,
    reasoning=args.reason,
    price=args.price,
)

print(f"\nResult: {result['status']}")

if result["status"] == "BLOCKED":
    print("Blocked reasons:")
    for r in result.get("reasons", []):
        print(f"  - {r}")
elif result["status"] == "LIVE":
    print(f"  Price: {result.get('price', 'N/A'):.3f} per share")
    print(f"  Shares: {result.get('size', 'N/A'):.1f}")
    print(f"  Order ID: {result.get('order_id', 'N/A')}")
    print(f"  Remaining balance: ${result.get('balance', 0):.2f}")
elif result["status"] == "FAILED":
    print(f"  Error: {result.get('error', 'Unknown')}")
