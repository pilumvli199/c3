def detect_candlestick_pattern(candles):
    if len(candles) < 3:
        return "No pattern"
    prev2, prev1, curr = candles[-3], candles[-2], candles[-1]
    if prev1['close'] < prev1['open'] and curr['close'] > curr['open'] and curr['close'] > prev1['open'] and curr['open'] < prev1['close']:
        return "Bullish Engulfing"
    elif prev1['close'] > prev1['open'] and curr['close'] < curr['open'] and curr['open'] > prev1['close'] and curr['close'] < prev1['open']:
        return "Bearish Engulfing"
    body = abs(curr['close'] - curr['open'])
    lower_wick = min(curr['open'], curr['close']) - curr['low']
    upper_wick = curr['high'] - max(curr['open'], curr['close'])
    if lower_wick > (2 * body) and upper_wick < body:
        return "Hammer"
    if upper_wick > (2 * body) and lower_wick < body:
        return "Shooting Star"
    if abs(curr['close'] - curr['open']) <= (0.1 * (curr['high'] - curr['low'])):
        return "Doji"
    return "No clear pattern"
