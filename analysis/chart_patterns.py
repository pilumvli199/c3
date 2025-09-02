def prepare_chart_points(candles, lookback=10):
    highs = [c['high'] for c in candles[-lookback:]]
    lows = [c['low'] for c in candles[-lookback:]]
    return {"highs": highs, "lows": lows}
