def detect_sr_levels(candles, deribit_data=None, lookback=20):
    if len(candles) < lookback:
        return "Not enough data"
    highs = [c['high'] for c in candles[-lookback:]]
    lows = [c['low'] for c in candles[-lookback:]]
    support = min(lows)
    resistance = max(highs)
    if deribit_data is not None and not deribit_data.empty:
        try:
            oi_group = deribit_data.groupby("strike")["oi"].sum()
            if not oi_group.empty:
                max_put_strike = oi_group.idxmax()
                max_call_strike = oi_group.idxmin()
                support = (support + max_put_strike) / 2 if max_put_strike else support
                resistance = (resistance + max_call_strike) / 2 if max_call_strike else resistance
        except Exception as e:
            print(f"⚠️ OI integration error: {e}")
    return f"Support: {round(support)}, Resistance: {round(resistance)}"
