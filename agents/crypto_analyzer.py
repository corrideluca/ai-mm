"""Crypto 5-min market analyzer with technical indicators.
Uses real-time price data to predict short-term direction before betting."""

import time
import requests
import json
from statistics import mean


def get_recent_prices(coin: str, minutes: int = 15) -> list[float]:
    """Get recent minute-by-minute prices from CoinGecko."""
    coin_map = {
        'btc': 'bitcoin',
        'eth': 'ethereum',
        'sol': 'solana',
        'xrp': 'ripple',
    }
    cg_id = coin_map.get(coin, coin)
    try:
        # CoinGecko market_chart for last 1 hour (gives ~minute granularity)
        resp = requests.get(
            f'https://api.coingecko.com/api/v3/coins/{cg_id}/market_chart',
            params={'vs_currency': 'usd', 'days': '0.01'},  # ~15 min
            timeout=5,
        )
        data = resp.json()
        prices = [p[1] for p in data.get('prices', [])]
        return prices[-minutes:] if len(prices) > minutes else prices
    except Exception:
        return []


def get_binance_klines(symbol: str, interval: str = '1m', limit: int = 15) -> list[dict]:
    """Get recent klines from Binance (more reliable, faster)."""
    try:
        resp = requests.get(
            'https://api.binance.com/api/v3/klines',
            params={'symbol': symbol, 'interval': interval, 'limit': limit},
            timeout=5,
        )
        klines = resp.json()
        return [
            {
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5]),
            }
            for k in klines
        ]
    except Exception:
        return []


BINANCE_SYMBOLS = {
    'btc': 'BTCUSDT',
    'eth': 'ETHUSDT',
    'sol': 'SOLUSDT',
    'xrp': 'XRPUSDT',
}


def calculate_momentum(prices: list[float]) -> float:
    """Simple momentum: % change over the period. Positive = uptrend."""
    if len(prices) < 2:
        return 0.0
    return (prices[-1] - prices[0]) / prices[0] * 100


def calculate_rsi(prices: list[float], period: int = 14) -> float:
    """Relative Strength Index. >70 = overbought (expect down), <30 = oversold (expect up)."""
    if len(prices) < period + 1:
        return 50.0  # neutral
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas[-period:]]
    losses = [-d if d < 0 else 0 for d in deltas[-period:]]
    avg_gain = mean(gains) if gains else 0
    avg_loss = mean(losses) if losses else 0.001
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_short_ema(prices: list[float], period: int = 5) -> float:
    """Exponential Moving Average for short-term trend."""
    if not prices:
        return 0.0
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = (p - ema) * multiplier + ema
    return ema


def analyze_coin(coin: str) -> dict:
    """Full analysis of a coin's short-term direction.
    Returns: {direction: 'UP'|'DOWN'|'NEUTRAL', confidence: 0-100, indicators: {...}}
    """
    symbol = BINANCE_SYMBOLS.get(coin)
    if not symbol:
        return {'direction': 'NEUTRAL', 'confidence': 0, 'reason': 'unknown coin'}

    # Get 15 1-minute candles from Binance
    klines = get_binance_klines(symbol, '1m', 15)
    if len(klines) < 5:
        return {'direction': 'NEUTRAL', 'confidence': 0, 'reason': 'no data'}

    closes = [k['close'] for k in klines]
    volumes = [k['volume'] for k in klines]
    current_price = closes[-1]

    # Indicators
    momentum_5m = calculate_momentum(closes[-5:])  # last 5 min
    momentum_15m = calculate_momentum(closes)  # last 15 min
    rsi = calculate_rsi(closes)
    ema5 = calculate_short_ema(closes, 5)
    ema10 = calculate_short_ema(closes, 10)
    vol_recent = mean(volumes[-3:]) if len(volumes) >= 3 else 0
    vol_avg = mean(volumes) if volumes else 1
    vol_spike = vol_recent / vol_avg if vol_avg > 0 else 1

    # Score system: positive = UP, negative = DOWN
    score = 0
    reasons = []

    # 1. Short-term momentum (strongest signal for 5-min)
    if momentum_5m > 0.05:
        score += 2
        reasons.append(f'5m momentum +{momentum_5m:.3f}%')
    elif momentum_5m < -0.05:
        score -= 2
        reasons.append(f'5m momentum {momentum_5m:.3f}%')

    # 2. Medium momentum confirmation
    if momentum_15m > 0.1:
        score += 1
        reasons.append(f'15m trend UP')
    elif momentum_15m < -0.1:
        score -= 1
        reasons.append(f'15m trend DOWN')

    # 3. EMA crossover
    if ema5 > ema10:
        score += 1
        reasons.append('EMA5 > EMA10 (bullish)')
    elif ema5 < ema10:
        score -= 1
        reasons.append('EMA5 < EMA10 (bearish)')

    # 4. RSI extremes (mean reversion)
    if rsi > 70:
        score -= 1
        reasons.append(f'RSI {rsi:.0f} overbought')
    elif rsi < 30:
        score += 1
        reasons.append(f'RSI {rsi:.0f} oversold')

    # 5. Volume spike (confirms trend)
    if vol_spike > 1.5:
        if score > 0:
            score += 1
        elif score < 0:
            score -= 1
        reasons.append(f'volume spike {vol_spike:.1f}x')

    # 6. Price vs last candle (micro-trend)
    last_candle = klines[-1]
    if last_candle['close'] > last_candle['open']:
        score += 1
        reasons.append('last candle green')
    elif last_candle['close'] < last_candle['open']:
        score -= 1
        reasons.append('last candle red')

    # Determine direction and confidence
    if score >= 2:
        direction = 'UP'
        confidence = min(score * 15, 80)
    elif score <= -2:
        direction = 'DOWN'
        confidence = min(abs(score) * 15, 80)
    else:
        direction = 'NEUTRAL'
        confidence = 20

    return {
        'direction': direction,
        'confidence': confidence,
        'score': score,
        'price': current_price,
        'momentum_5m': momentum_5m,
        'momentum_15m': momentum_15m,
        'rsi': rsi,
        'ema_cross': 'bullish' if ema5 > ema10 else 'bearish',
        'vol_spike': vol_spike,
        'reasons': reasons,
    }


def analyze_all() -> dict:
    """Analyze all 4 coins and return trading signals."""
    results = {}
    for coin in ['btc', 'eth', 'sol', 'xrp']:
        results[coin] = analyze_coin(coin)
    return results


if __name__ == '__main__':
    print("=== Crypto 5-Min Analysis ===\n")
    signals = analyze_all()
    for coin, sig in signals.items():
        arrow = '^' if sig['direction'] == 'UP' else ('v' if sig['direction'] == 'DOWN' else '-')
        print(f"{coin.upper()} {arrow} {sig['direction']} (conf: {sig['confidence']}%, score: {sig['score']})")
        print(f"  Price: ${sig['price']:,.2f} | Mom5m: {sig['momentum_5m']:.3f}% | RSI: {sig['rsi']:.0f}")
        print(f"  EMA: {sig['ema_cross']} | Vol: {sig['vol_spike']:.1f}x")
        print(f"  Reasons: {', '.join(sig['reasons'])}")
        print()
