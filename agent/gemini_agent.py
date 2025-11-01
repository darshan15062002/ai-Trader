import google.generativeai as genai
import os, json

# Configure Gemini API
genai.configure(api_key="AIzaSyAfjsA-tRRq6iBmlvX1abOmZgIDweq_Hwg")

def decide_action(agent_name, portfolio, stock_data, cash_available):
    """
    Ask Gemini for a trading decision.
    """
    prompt = f"""
    You are a trading agent named {agent_name}.
    The portfolio and current cash are below.
    Decide whether to BUY, SELL, or HOLD for each stock.
    Your goal is to maximize long-term profit while managing risk.

    Portfolio: {json.dumps(portfolio, indent=2)}
    Cash Available: ₹{cash_available}
    Stock Indicators:
    {json.dumps(stock_data, indent=2)}

    Use these signals:
    - SMA_20 vs SMA_50: trend direction
    - RSI_14: overbought/oversold
    - MACD, MACD_signal, MACD_diff: momentum

    Respond ONLY in JSON format like this:
    {{
        "decisions": [
            {{"symbol": "RELIANCE", "action": "BUY", "quantity": 5}},
            {{"symbol": "TCS", "action": "HOLD", "quantity": 0}}
        ]
    }}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    try:
        text = response.text.strip()
        decision_data = json.loads(text)
        return decision_data
    except Exception as e:
        print("⚠️ Error parsing Gemini response:", e)
        print("Raw output:", response.text)
        return {"decisions": []}
