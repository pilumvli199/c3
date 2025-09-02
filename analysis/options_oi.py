def analyze_options(deribit_data):
    if deribit_data is None or deribit_data.empty:
        return "No options data"
    try:
        call_oi = deribit_data[deribit_data["option_type"] == "call"]["oi"].sum()
        put_oi = deribit_data[deribit_data["option_type"] == "put"]["oi"].sum()
        avg_iv = deribit_data["iv"].mean()
        if put_oi > call_oi * 1.2:
            bias = "Bullish (Put OI buildup)"
        elif call_oi > put_oi * 1.2:
            bias = "Bearish (Call OI buildup)"
        else:
            bias = "Neutral (balanced OI)"
        return f"{bias}, Avg IV: {round(avg_iv*100, 2)}%"
    except Exception as e:
        return "Options analysis failed"
