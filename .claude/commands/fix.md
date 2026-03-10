Diagnose and fix issues with the bot. Run this when something breaks.

If an error was provided: $ARGUMENTS

## Step 1: Check environment
```
cd /Users/corri/polymarket-agent && python3 -c "
import sys
print(f'Python: {sys.executable} ({sys.version})')
print(f'Venv active: {sys.prefix != sys.base_prefix}')
"
```

If venv is not active:
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "print('venv activated OK')"
```

## Step 2: Check dependencies
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "
errors = []
for pkg in ['py_clob_client', 'dotenv', 'web3', 'rich']:
    try:
        __import__(pkg)
    except ImportError as e:
        errors.append(str(e))
if errors:
    print('MISSING PACKAGES:')
    for e in errors:
        print(f'  - {e}')
    print('\nFix: pip install -r requirements.txt')
else:
    print('All packages OK')
"
```

If packages are missing:
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && pip install -r requirements.txt
```

## Step 3: Check .env config
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "
from core.config import config
checks = {
    'Private key': bool(config.private_key),
    'Funder address': bool(config.funder_address),
    'Chain ID': config.chain_id == 137,
    'CLOB URL': 'polymarket.com' in config.clob_url,
}
for name, ok in checks.items():
    print(f'  {\"OK\" if ok else \"FAIL\"} {name}')
if not all(checks.values()):
    print('\nCheck your .env file — some config is missing')
"
```

## Step 4: Check API connectivity
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "
from core.client import get_public_client, get_wallet_balance
try:
    pub = get_public_client()
    markets = pub.get_markets()
    print(f'  OK API connection ({len(markets.get(\"data\", []))} markets)')
except Exception as e:
    print(f'  FAIL API: {e}')
try:
    w = get_wallet_balance()
    print(f'  OK Wallet: {w[\"usdc_e\"]:.2f} USDC.e, {w[\"pol\"]:.4f} POL')
except Exception as e:
    print(f'  FAIL Wallet: {e}')
"
```

## Step 5: Check auth client (trading)
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "
from core.client import get_authenticated_client, get_balance
try:
    client = get_authenticated_client()
    bal = get_balance(client)
    print(f'  OK Auth client (balance: {bal})')
except Exception as e:
    print(f'  FAIL Auth: {e}')
"
```

## Step 6: Check cache health
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "
from pathlib import Path
import json, time
cache_dir = Path('.cache')
if not cache_dir.exists():
    print('  No cache dir (OK — will be created on first use)')
else:
    files = list(cache_dir.glob('*.json'))
    stale = 0
    for f in files:
        try:
            data = json.loads(f.read_text())
            if time.time() - data['ts'] > 300:
                stale += 1
        except:
            stale += 1
    print(f'  Cache: {len(files)} entries, {stale} stale')
    if stale > 0:
        print('  Consider running /clear-cache')
"
```

## Step 7: Check risk state
```
cd /Users/corri/polymarket-agent && source .venv/bin/activate && python3 -c "
from agents.risk import get_daily_pnl
from core.config import config
pnl = get_daily_pnl()
print(f'  Daily P&L: \${pnl:.2f}')
print(f'  Daily loss limit: {config.risk.daily_loss_pct*100:.0f}% of balance')
if pnl < 0:
    print('  ⚠ In the red today — risk manager may block trades')
"
```

## After all checks:
- Summarize what's working and what's broken
- If there's a specific error from $ARGUMENTS, diagnose the root cause
- Fix any issues you can (install packages, clear stale cache, etc.)
- If it's an .env or wallet issue, tell the user what to fix manually
- If a Python file has a bug, read it, fix it, and test the fix
