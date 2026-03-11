# 5-Minute Quickstart

## Step 1: Get Your Polymarket Private Key

1. Go to [polymarket.com](https://polymarket.com)
2. Connect your wallet (MetaMask recommended)
3. Export your private key from MetaMask:
   - MetaMask → Account → Settings → Security → Export Private Key
4. Fund your wallet with USDC on Polygon network

## Step 2: Set Up the Bot

```bash
# Clone or extract this kit into a directory
cd polymarket-starter-kit

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Mac/Linux
# .venv\Scripts\activate       # Windows

# Install dependencies (takes ~30 seconds)
pip install -r requirements.txt

# Set up credentials
cp .env.example .env
```

Edit `.env` and replace:
- `your_private_key_here` → your MetaMask private key (starts with `0x`)
- `0xYourWalletAddressHere` → your wallet address

## Step 3: Test Your Connection

```bash
python examples/check_portfolio.py
```

Expected output:
```
Balance: $X.XX USDC
Open orders: 0
Positions: 0
```

If you see your balance, you're connected!

## Step 4: Scan for Opportunities

```bash
python examples/scan_markets.py
```

This shows all markets resolving in the next 48 hours. Look for:
- Markets where you have strong conviction
- Prices that seem off (e.g., market says 30%, you think it's 60%)

## Step 5: Place Your First Trade

```bash
python examples/place_trade.py --token-id TOKEN_ID --amount 5 --side BUY
```

Or use the trader directly in Python:

```python
from agents.trader import execute_trade

result = execute_trade(
    token_id="your_token_id_here",
    amount=5.00,           # $5 USDC
    side="BUY",
    market_name="Will X happen?",
    reasoning="Strong precursor data + 10c edge",
)
print(result)
```

## Step 6: Integrate with AI

For the full AI-powered workflow, copy the output of `scan_markets.py` into Claude Code and ask:

```
"Which of these markets are mispriced based on your knowledge?
What would you bet and why?"
```

Then execute the trades it recommends using `execute_trade()`.

## Common Issues

**"Balance is $0"** → Fund your wallet with USDC on Polygon network

**"BLOCKED: Daily loss limit"** → Wait until next day or increase `DAILY_LOSS_PCT` in `.env`

**"Order FAILED"** → Minimum order is $5 and 5 shares. Check your balance.

**Import errors** → Make sure your virtual environment is activated (`source .venv/bin/activate`)

---

Need help? DM [@agent_20usd](https://x.com/agent_20usd) on X.
