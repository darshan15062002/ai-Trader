import google.generativeai as genai
import os, json

# Configure Gemini API
genai.configure(api_key="AIzaSyAfjsA-tRRq6iBmlvX1abOmZgIDweq_Hwg")

def clean_model_output(raw_text: str) -> str:
    """
    Clean Gemini output so it's pure JSON.
    Handles code blocks like ```json ... ```, stray text, or spaces.
    """
    text = raw_text.strip()

    # Remove Markdown code fences
    if text.startswith("```"):
        # remove leading and trailing triple backticks
        text = text.strip("`")
        # remove possible 'json' tag
        text = text.replace("json", "", 1).strip()
    # In case Gemini adds markdown fencing inside
    text = text.replace("```json", "").replace("```", "").strip()
    return text
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
    

    #IMPORTANT : Return ONLY valid JSON — no explanation, no markdown, no commentary.

    {{
        "decisions": [
            {{"symbol": "RELIANCE", "action": "BUY", "quantity": 5}},
            {{"symbol": "TCS", "action": "HOLD", "quantity": 0}}
        ]
    }}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    try:
        text = clean_model_output(response.text)
        decision_data = json.loads(text)
        return decision_data
    except Exception as e:
        print("⚠️ Error parsing Gemini response:", e)
        print("Raw output:", response.text)
        return {"decisions": []}
