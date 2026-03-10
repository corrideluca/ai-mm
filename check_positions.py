import requests, json
resp = requests.get('https://data-api.polymarket.com/positions?user=0x30fe68A3CF68302A42beC4DC739aa2Ed3bf6aBD2', timeout=15)
data = resp.json()
total_value = sum(p.get('currentValue', 0) for p in data)
total_invested = sum(p.get('initialValue', 0) for p in data)
print(f'Total positions: {len(data)}')
print(f'Total invested: ${total_invested:.2f}')
print(f'Total current value: ${total_value:.2f}')
print(f'Unrealized P&L: ${total_value - total_invested:.2f}')
print()
for p in data:
    redeemable = p.get('redeemable', False)
    status = 'REDEEMABLE' if redeemable else 'LIVE'
    print(f"[{status}] {p['title'][:65]} | {p['outcome']} | size={p['size']:.2f} | cur={p['curPrice']:.3f} | val=${p['currentValue']:.2f} | pnl={p['percentPnl']:.1f}%")
