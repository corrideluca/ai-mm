# ai-risk-calc

[![npm version](https://img.shields.io/npm/v/ai-risk-calc.svg)](https://www.npmjs.com/package/ai-risk-calc)
[![license](https://img.shields.io/npm/l/ai-risk-calc.svg)](https://opensource.org/licenses/MIT)

**CLI position sizing calculator for traders.** Calculate optimal bet sizes using fixed-risk percentage or Kelly Criterion. Works for crypto, stocks, prediction markets, forex, and sports betting.

Zero dependencies. Just math.

## Install

```bash
npm install -g ai-risk-calc
```

## Quick Start

```bash
# Basic position sizing
ai-risk-calc --balance 10000 --risk 2 --entry 50 --stop 45

# With target price for Risk:Reward analysis
ai-risk-calc --balance 10000 --entry 50 --stop 45 --target 65

# Kelly Criterion optimal sizing
ai-risk-calc --kelly --balance 10000 --win-rate 0.6 --avg-win 1.5 --avg-loss 1

# Interactive mode (guided prompts)
ai-risk-calc
```

## Position Sizing

Calculates how many shares/units to buy based on your acceptable risk.

```bash
ai-risk-calc --balance 1000 --risk 2 --entry 50 --stop 45
```

```
  ╔══════════════════════════════════════╗
  ║   ai-risk-calc v1.0.0               ║
  ║   Position Sizing Calculator         ║
  ╚══════════════════════════════════════╝

  POSITION SIZING
  ─────────────────────────────────────
  Direction:        LONG
  Entry Price:      $50
  Stop Loss:        $45
  ─────────────────────────────────────
  Shares/Units:     4
  Position Value:   $200  (20% of balance)
  Dollar at Risk:   $20  (2% of balance)
  Risk per Share:   $5
```

### With Target Price

```bash
ai-risk-calc --balance 10000 --entry 150 --stop 140 --target 180
```

Adds Risk:Reward ratio analysis:

```
  REWARD : RISK
  ─────────────────────────────────────
  R:R Ratio:        3:1
  Potential Profit: +$600  (6% of balance)
  * Excellent risk/reward setup
```

## Kelly Criterion

Find the mathematically optimal bet size for repeated bets.

```bash
ai-risk-calc --kelly --balance 10000 --win-rate 0.6 --avg-win 1.5 --avg-loss 1
```

```
  KELLY CRITERION
  ─────────────────────────────────────
  Win Rate:         60%
  Avg Win:          1.5
  Avg Loss:         1
  Edge:             40%
  Expected Value:   0.5  per dollar risked
  ─────────────────────────────────────

  RECOMMENDED SIZING
  ─────────────────────────────────────
  Full Kelly:       26.67%  = $2666.67  (aggressive)
  Half Kelly:       13.33%  = $1333.33  (recommended)
  Quarter Kelly:    6.67%   = $666.67   (conservative)

  * Half Kelly is generally recommended for most traders
  * Full Kelly maximizes growth but has high variance
```

## Options

### Position Sizing Mode

| Flag | Description | Default |
|------|-------------|---------|
| `--balance <num>` | Portfolio balance | *required* |
| `--risk <num>` | Risk per trade (%) | `2` |
| `--max-position <num>` | Max position as % of balance | `20` |
| `--entry <num>` | Entry price | *required* |
| `--stop <num>` | Stop loss price | *required* |
| `--target <num>` | Target price for R:R | *optional* |

### Kelly Criterion Mode

| Flag | Description |
|------|-------------|
| `--kelly` | Enable Kelly mode |
| `--balance <num>` | Portfolio balance |
| `--win-rate <num>` | Win rate as decimal (e.g. 0.6) |
| `--avg-win <num>` | Average win amount/multiplier |
| `--avg-loss <num>` | Average loss amount/multiplier |

### General

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON (for piping to other tools) |
| `--help, -h` | Show help |
| `--version, -v` | Show version |

## JSON Output

Pipe results into other tools:

```bash
ai-risk-calc --balance 1000 --entry 50 --stop 45 --json
```

```json
{
  "direction": "LONG",
  "shares": 4,
  "positionValue": 200,
  "positionPercent": 20,
  "dollarRisk": 20,
  "riskPercent": 2,
  "riskPerShare": 5,
  "entry": 50,
  "stop": 45,
  "capped": false
}
```

## Use Cases

- **Crypto trading** — Size your BTC/ETH positions based on account risk
- **Stock trading** — Calculate share counts for swing trades
- **Prediction markets** — Size bets on Polymarket, Kalshi, etc.
- **Forex** — Position sizing for currency pairs
- **Sports betting** — Kelly Criterion for handicapping edges
- **Options** — Risk-based position sizing for premium selling

## The Math

### Position Sizing Formula

```
Dollar Risk = Balance * (Risk% / 100)
Risk Per Share = |Entry - Stop|
Shares = Dollar Risk / Risk Per Share
Position Value = Shares * Entry
```

If position value exceeds the max-position limit, shares are reduced to fit.

### Kelly Criterion Formula

```
f* = (p * b - q) / b

where:
  p = probability of winning
  q = 1 - p (probability of losing)
  b = average win / average loss
```

Half Kelly (`f*/2`) is recommended for most traders as it captures 75% of the growth rate with significantly less variance.

## Programmatic Usage

```js
const { calculatePosition, calculateKelly } = require('ai-risk-calc/lib/calculator');

const position = calculatePosition({
  balance: 10000,
  riskPercent: 2,
  maxPosition: 20,
  entry: 50,
  stop: 45,
  target: 65,
});

console.log(position.shares);        // 40
console.log(position.dollarRisk);    // 200
console.log(position.rewardRiskRatio); // 3

const kelly = calculateKelly({
  balance: 10000,
  winRate: 0.6,
  avgWin: 1.5,
  avgLoss: 1,
});

console.log(kelly.halfKelly);       // 13.33
console.log(kelly.halfKellyAmount); // 1333.33
```

## License

MIT
