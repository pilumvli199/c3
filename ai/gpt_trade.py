from openai import OpenAI
import json
import re

# Initialize OpenAI client (reads OPENAI_API_KEY from env automatically)
client = OpenAI()

def get_signal(summary: dict, risk_reward=2):
    """
    Uses GPT-4o-mini to generate trading signal based on market summary.
    Ensures JSON parsing works even if GPT wraps output in ```json ... ``` fences.
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
        # Call GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        # Raw text
        raw_text = response.choices[0].message.content.strip()
        print(f"🔍 GPT Raw Response: {raw_text}")

        # --- Clean response ---
        # Remove markdown code fences like ```json ... ```
        cleaned = re.sub(r"```(json)?", "", raw_text).strip("` \n")

        # Parse JSON safely
        return json.loads(cleaned)

    except Exception as e:
        print(f"⚠️ GPT error: {e}")
        return None
