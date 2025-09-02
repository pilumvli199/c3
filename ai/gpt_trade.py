import openai, json

def get_signal(summary: dict, risk_reward=2):
    prompt = f"""Symbol: {summary['symbol']}
Price Action: {summary['price_action']}
Support/Resistance: {summary['support_resistance']}
Candlestick: {summary['candlestick']}
Volume: {summary['volume']}
OI/IV: {summary['oi_iv']}

Task: Decide BUY/SELL/HOLD with Confidence %, Entry, Target, StopLoss.
Rules: Risk-Reward {risk_reward}:1. Respond JSON only."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        raw_text = response["choices"][0]["message"]["content"].strip()
        return json.loads(raw_text)
    except Exception as e:
        print(f"⚠️ GPT error: {e}")
        return None
