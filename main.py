import time
import schedule
from config import FULL_COINS, LITE_COINS, CONFIDENCE_THRESHOLD
from data_sources.binance_api import get_ohlcv, get_volume
from data_sources.deribit_api import fetch_data as fetch_deribit
from analysis.price_action import detect_price_action
from analysis.candlesticks import detect_candlestick_pattern
from analysis.support_resistance import detect_sr_levels
from analysis.chart_patterns import prepare_chart_points
from analysis.options_oi import analyze_options
from analysis.confidence import calc_confidence
from ai.gpt_trade import get_signal
from alerts.telegram_bot import safe_send

def scan_coins():
    print("🔄 Running swing scan...")

    for coin in FULL_COINS:
        try:
            candles = get_ohlcv(coin, interval="30m", limit=50)
            volume = get_volume(coin)
            deribit_data = fetch_deribit(coin.split("USDT")[0])

            pa = detect_price_action(candles)
            cs = detect_candlestick_pattern(candles)
            sr = detect_sr_levels(candles, deribit_data)
            cp = prepare_chart_points(candles)
            oi_iv = analyze_options(deribit_data)

            summary = {
                "symbol": coin,
                "price_action": pa,
                "support_resistance": sr,
                "candlestick": cs,
                "volume": volume,
                "oi_iv": oi_iv
            }

            confidence = calc_confidence(summary, full_coin=True)
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            signal = get_signal(summary, risk_reward=2)
            if signal:
                signal["symbol"] = coin
                signal["confidence"] = confidence
                safe_send(signal)

        except Exception as e:
            print(f"⚠️ Error scanning {coin}: {e}")

    for coin in LITE_COINS:
        try:
            candles = get_ohlcv(coin, interval="30m", limit=50)
            volume = get_volume(coin)

            pa = detect_price_action(candles)
            cs = detect_candlestick_pattern(candles)
            sr = detect_sr_levels(candles, None)
            cp = prepare_chart_points(candles)

            summary = {
                "symbol": coin,
                "price_action": pa,
                "support_resistance": sr,
                "candlestick": cs,
                "volume": volume,
                "oi_iv": "N/A"
            }

            confidence = calc_confidence(summary, full_coin=False)
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            signal = get_signal(summary, risk_reward=2)
            if signal:
                signal["symbol"] = coin
                signal["confidence"] = confidence
                safe_send(signal)

        except Exception as e:
            print(f"⚠️ Error scanning {coin}: {e}")

def run_scheduler():
    # Send Telegram startup message
    from alerts.telegram_bot import safe_send
    safe_send({
        "symbol": "SYSTEM",
        "action": "INFO",
        "confidence": 100,
        "entry": "-",
        "target": "-",
        "stoploss": "-",
        "reason": "🚀 Bot Started Successfully!"
    })
    schedule.every(30).minutes.do(scan_coins)
    schedule.every().hour.do(scan_coins)
    print("✅ Swing Bot started (scans every 30m & 1h)...")
    while True:
        schedule.run_pending()
        time.sleep(5)

if __name__ == "__main__":
    run_scheduler()
