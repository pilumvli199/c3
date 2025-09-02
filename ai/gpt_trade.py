from openai import OpenAI
import json

client = OpenAI()

def get_signal(summary: dict, risk_reward=2):
    prompt = f"""Symbol: {summary['symbol']}
Price Action: {summary['price_action']}
Support/Resistance: {summary['support_resistance']}
Candlestick: {summary['candlestick']}
Volume: {summary['volume']}
OI/IV: {summary['oi_iv']}

Task: Decide BUY/SELL/HOLD with Confidence %, Entry, Target, StopLoss.
Rules: Risk-Reward {risk_reward}:1. Respond JSON only in format:
{{
  "action": "BUY/SELL/HOLD",
  "confidence": 75,
  "entry": 26350,
  "target": 26800,
  "stoploss": 26100,
  "reason": "Uptrend + bullish engulfing"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        raw_text = response.choices[0].message.content.strip()

        # Debug log
        print(f"🔍 GPT Raw Response: {raw_text}")

        # Try to parse JSON safely
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON, returning None")
            return None

    except Exception as e:
        print(f"⚠️ GPT error: {e}")
        return None

