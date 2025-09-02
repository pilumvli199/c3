from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI()

def get_signal(summary: dict, risk_reward=2):
    """
    Uses GPT-4o-mini to generate trading signal based on summary.
    Compatible with openai>=1.0.0 SDK.
    """

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

        # Try to parse JSON
        return json.loads(raw_text)

    except Exception as e:
        print(f"⚠️ GPT error: {e}")
        return None
