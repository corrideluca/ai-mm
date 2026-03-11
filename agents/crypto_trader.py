"""Non-stop 5-min crypto trader with technical analysis.
Run: python agents/crypto_trader.py [rounds]

RULES:
- NEVER bet blind. Only bet when TA score >= 3 (strong signal)
- Bet ALL coins with strong signals (more edge bets = more profit)
- Cap total exposure at 50% of balance per window
- Use market orders for instant fills (no frozen cash)
"""
import sys
import time
import requests
import json
from core.client import place_market_order, place_limit_order, get_balance
from agents.crypto_analyzer import analyze_all

COINS = ['btc', 'eth', 'sol', 'xrp']

MIN_SCORE = 3        # Need score >= 3 to trade
HIGH_CONF_SCORE = 4  # Score >= 4 = bigger bet
MAX_WINDOW_EXPOSURE = 0.50  # Max 50% of balance per window across all bets


def get_market_tokens(coin, window):
    """Get token IDs for a 5-min market window."""
    slug = f"{coin}-updown-5m-{window}"
    try:
        resp = requests.get(
            f"https://gamma-api.polymarket.com/events?slug={slug}", timeout=8
        )
        events = resp.json()
        if not events:
            return None
        m = events[0]['markets'][0]
        raw = m.get('clobTokenIds')
        tids = json.loads(raw) if isinstance(raw, str) else raw
        return tids
    except Exception:
        return None


def trade_window():
    """Analyze all coins, bet ALL with strong signals."""
    bal = get_balance()
    now = int(time.time())
    window = (now // 300) * 300
    remaining = (window + 300) - now

    print(f"\nBalance: ${bal:.2f} | Window: {window} | {remaining}s left")

    if bal < 1.0:
        print("  !! Balance too low to trade.")
        return 0

    # Run technical analysis
    signals = analyze_all()
    for c, s in signals.items():
        d = s['direction']
        tag = '^' if d == 'UP' else ('v' if d == 'DOWN' else '-')
        print(f"  {c.upper()} {tag} {d} score={s['score']} conf={s['confidence']}% | {', '.join(s['reasons'][:3])}")

    # Collect all tradeable signals, sorted by strength
    tradeable = []
    for coin in COINS:
        sig = signals.get(coin, {})
        score = abs(sig.get('score', 0))
        if sig.get('direction', 'NEUTRAL') != 'NEUTRAL' and score >= MIN_SCORE:
            tradeable.append((coin, sig, score))
    tradeable.sort(key=lambda x: x[2], reverse=True)

    if not tradeable:
        print("  -- No strong signals. Skipping. (Patience = profit)")
        return 0

    # Budget: split exposure across all tradeable coins
    max_total = bal * MAX_WINDOW_EXPOSURE
    num_bets = len(tradeable)
    traded = 0

    for coin, sig, score in tradeable:
        direction = sig['direction']
        tids = get_market_tokens(coin, window)
        if not tids:
            print(f"  {coin.upper()}: no market found")
            continue

        # Per-coin budget: divide evenly, but give more to higher scores
        if score >= HIGH_CONF_SCORE:
            bet_amount = max_total * 0.30 if num_bets > 1 else max_total * 0.50
        else:
            bet_amount = max_total / num_bets

        bet_amount = max(bet_amount, 2.50)
        bet_amount = min(bet_amount, bal * 0.20)  # Still cap per coin at 20%

        token = tids[0] if direction == 'UP' else tids[1]
        shares = max(5, int(bet_amount / 0.50))
        price = 0.52 if score >= HIGH_CONF_SCORE else 0.50

        # Try market order first (instant fill, no frozen cash)
        try:
            result = place_market_order(token, bet_amount, 'BUY')
            status = getattr(result, 'status', str(result)[:50])
            print(f"  >> {coin.upper()} {direction} ${bet_amount:.2f} MARKET: {status}")
            traded += 1
        except Exception as e:
            # Fallback to aggressive limit order
            try:
                result = place_limit_order(token, price, shares, 'BUY')
                status = 'MATCHED' if result.status == 'matched' else result.status
                print(f"  >> {coin.upper()} {direction} {shares}@{price} LIMIT: {status}")
                traded += 1
            except Exception as e2:
                print(f"  >> {coin.upper()} {direction}: FAILED {str(e2)[:60]}")

    if traded == 0:
        print("  -- Orders failed. Will retry next window.")

    return traded


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    start_bal = get_balance()
    total_trades = 0
    wins = 0
    losses = 0

    print(f"=== NON-STOP TA TRADER ===")
    print(f"Starting balance: ${start_bal:.2f}")
    print(f"Rounds: {rounds} | Min score: {MIN_SCORE}")
    print(f"Bet ALL strong signals | Max {MAX_WINDOW_EXPOSURE*100:.0f}% exposure/window\n")

    for i in range(rounds):
        # Wait until ~90s into next window
        now = int(time.time())
        window = (now // 300) * 300
        entry = window + 90
        if now >= entry:
            entry = window + 300 + 90
        wait = entry - now
        if wait > 0 and i > 0:
            print(f"\n--- Waiting {wait}s for next entry ---")
            time.sleep(wait)

        print(f"\n{'='*50}")
        print(f"ROUND {i + 1}/{rounds}")
        print(f"{'='*50}")

        pre_bal = get_balance()
        num_trades = trade_window()
        total_trades += num_trades

        if num_trades > 0:
            # Wait for window to resolve
            now2 = int(time.time())
            w2 = (now2 // 300) * 300
            resolve_wait = (w2 + 300) - now2 + 10
            print(f"  Waiting {resolve_wait}s for resolution...")
            time.sleep(resolve_wait)

            post_bal = get_balance()
            pnl = post_bal - pre_bal
            if pnl > 0.01:
                wins += 1
                print(f"  WIN! +${pnl:.2f} | Balance: ${post_bal:.2f}")
            elif pnl < -0.01:
                losses += 1
                print(f"  LOSS -${abs(pnl):.2f} | Balance: ${post_bal:.2f}")
            else:
                print(f"  FLAT | Balance: ${post_bal:.2f}")

            total = wins + losses
            wr = (wins / total * 100) if total > 0 else 0
            running_pnl = post_bal - start_bal
            print(f"  Record: {wins}W/{losses}L ({wr:.0f}% WR) | P&L: ${running_pnl:+.2f}")
        else:
            time.sleep(30)

    final_bal = get_balance()
    total_pnl = final_bal - start_bal
    print(f"\n{'='*50}")
    print(f"=== SESSION COMPLETE ===")
    print(f"Rounds: {rounds} | Trades: {total_trades}")
    print(f"Record: {wins}W / {losses}L")
    print(f"${start_bal:.2f} -> ${final_bal:.2f} (P&L: ${total_pnl:+.2f})")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
