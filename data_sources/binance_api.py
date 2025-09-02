import requests
import time

BINANCE_BASE = "https://api.binance.com/api/v3"

def safe_request(url, params=None, retries=3, delay=2):
    for attempt in range(retries):
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"⚠️ Binance API error (attempt {attempt+1}): {e}")
            time.sleep(delay)
    return None

def get_ohlcv(symbol="BTCUSDT", interval="30m", limit=50):
    url = f"{BINANCE_BASE}/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = safe_request(url, params)
    if not data:
        return []
    candles = []
    for c in data:
        candles.append({
            "time": c[0],
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        })
    return candles

def get_volume(symbol="BTCUSDT"):
    url = f"{BINANCE_BASE}/ticker/24hr"
    params = {"symbol": symbol}
    data = safe_request(url, params)
    if not data:
        return {"last_price": 0, "volume": 0, "price_change": 0}
    return {
        "last_price": float(data["lastPrice"]),
        "volume": float(data["volume"]),
        "price_change": float(data["priceChangePercent"])
    }
