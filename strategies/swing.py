from analysis.price_action import detect_price_action
from analysis.candlesticks import detect_candlestick_pattern

def swing_strategy(candles_30m, candles_1h):
    pa_30m = detect_price_action(candles_30m)
    pa_1h = detect_price_action(candles_1h)
    cs_30m = detect_candlestick_pattern(candles_30m)
    cs_1h = detect_candlestick_pattern(candles_1h)
    if pa_30m == "Uptrend" and pa_1h == "Uptrend":
        if "Bullish" in cs_30m or "Bullish" in cs_1h:
            return "BUY"
    elif pa_30m == "Downtrend" and pa_1h == "Downtrend":
        if "Bearish" in cs_30m or "Bearish" in cs_1h:
            return "SELL"
    return "HOLD"
