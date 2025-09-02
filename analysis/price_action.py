def detect_price_action(candles, lookback=10):
    if len(candles) < lookback:
        return "Not enough data"
    highs = [c['high'] for c in candles[-lookback:]]
    lows = [c['low'] for c in candles[-lookback:]]
    hh = all(highs[i] > highs[i-1] for i in range(1, len(highs)//2))
    hl = all(lows[i] > lows[i-1] for i in range(1, len(lows)//2))
    lh = all(highs[i] < highs[i-1] for i in range(1, len(highs)//2))
    ll = all(lows[i] < lows[i-1] for i in range(1, len(lows)//2))
    if hh and hl:
        return "Uptrend"
    elif lh and ll:
        return "Downtrend"
    else:
        return "Range"
