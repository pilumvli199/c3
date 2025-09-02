def score_price_action(pa): return 80 if "Uptrend" in pa else 40 if "Downtrend" in pa else 50
def score_support_resistance(sr): return 80 if "Support" in sr else 60
def score_candlestick(cs): return 75 if "Bullish" in cs else 45 if "Bearish" in cs else 60
def score_volume(vol): return 70 if "Rising" in vol else 40 if "Falling" in vol else 55
def score_oi_iv(oi): return 70 if "Bullish" in oi else 40 if "Bearish" in oi else 55

def calc_confidence(summary, full_coin=True):
    pa = score_price_action(summary.get("price_action", ""))
    sr = score_support_resistance(summary.get("support_resistance", ""))
    cs = score_candlestick(summary.get("candlestick", ""))
    vol = score_volume(summary.get("volume", ""))
    oi = score_oi_iv(summary.get("oi_iv", "")) if full_coin else 0
    weights = {"price_action":0.4,"support_resistance":0.25,"candlestick":0.2,"volume":0.15,"oi_iv":0.05 if full_coin else 0}
    total_weight = sum(weights.values())
    confidence = (pa*weights["price_action"]+sr*weights["support_resistance"]+cs*weights["candlestick"]+vol*weights["volume"]+oi*weights["oi_iv"])/total_weight
    return round(confidence)
