import requests
import time
import pandas as pd

DERIBIT_BASE = "https://www.deribit.com/api/v2"

def safe_request(url, params=None, retries=3, delay=2):
    for attempt in range(retries):
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            print(f"⚠️ Deribit API error (attempt {attempt+1}): {e}")
            time.sleep(delay)
    return None

def get_instruments(currency="BTC", kind="option"):
    url = f"{DERIBIT_BASE}/public/get_instruments"
    params = {"currency": currency, "kind": kind, "expired": "false"}
    data = safe_request(url, params)
    if not data:
        return []
    return data.get("result", [])

def get_book_summary(instrument):
    url = f"{DERIBIT_BASE}/public/get_book_summary_by_instrument"
    params = {"instrument_name": instrument}
    data = safe_request(url, params)
    if not data:
        return None
    return data.get("result", [None])[0]

def fetch_data(currency="BTC", limit=50):
    instruments = get_instruments(currency)
    if not instruments:
        return pd.DataFrame()
    chain_data = []
    for inst in instruments[:limit]:
        summary = get_book_summary(inst["instrument_name"])
        if not summary:
            continue
        greeks = summary.get("greeks", {})
        chain_data.append({
            "instrument": inst["instrument_name"],
            "strike": inst.get("strike"),
            "expiry": inst["expiration_timestamp"],
            "option_type": inst.get("option_type"),
            "oi": summary.get("open_interest", 0),
            "iv": summary.get("iv", 0),
            "delta": greeks.get("delta"),
            "gamma": greeks.get("gamma"),
            "theta": greeks.get("theta"),
            "vega": greeks.get("vega"),
        })
    return pd.DataFrame(chain_data)
