import os
import telebot
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def format_message(signal: dict):
    return (
        f"⚡ {signal['symbol']} Swing Signal\n"
        f"Action: {signal['action']}\n"
        f"Confidence: {signal['confidence']}%\n"
        f"Entry: {signal['entry']}\n"
        f"🎯 Target: {signal['target']}\n"
        f"🛑 StopLoss: {signal['stoploss']}\n"
        f"Reason: {signal['reason']}"
    )

def safe_send(signal: dict, retries=3):
    msg = format_message(signal)
    for attempt in range(retries):
        try:
            bot.send_message(CHAT_ID, msg)
            return True
        except Exception as e:
            print(f"⚠️ Telegram send failed (attempt {attempt+1}): {e}")
            time.sleep(2)
    return False
