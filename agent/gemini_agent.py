import google.generativeai as genai
import os, json

# Configure Gemini API
genai.configure(api_key="AIzaSyAfjsA-tRRq6iBmlvX1abOmZgIDweq_Hwg")

def analyze_signals(stock_data):
    prompt = f"""
    You are a technical analyst.
    For each stock, interpret the indicators into human-level reasoning.

    Convert raw indicators into:
      - trend_strength (0 to 1)
      - momentum_bias ("bullish", "bearish", "neutral")
      - risk_level ("low", "medium", "high")
      - rsi_state ("overbought", "oversold", "normal")

    Stock Indicators:
    {json.dumps(stock_data, indent=2)}

    Return only valid JSON like:
    {{
      "analysis": {{
         "RELIANCE": {{
            "trend_strength": 0.7,
            "momentum_bias": "bullish",
            "risk_level": "medium",
            "rsi_state": "normal"
         }}
      }}
    }}
    """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    try:
        text = clean_model_output(response.text)
        return json.loads(text)
    except:
        return {"analysis": {}}


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
    analysis = analyze_signals(stock_data)  # Optional: could use this for more context

    prompt = f"""
    You are a disciplined trading decision engine.
    Use the analysis provided to generate BUY, SELL or HOLD.

    Constraints:
      - Use cash efficiently
      - Avoid buying overbought stocks
      - Increase position if trend is strong
      - Sell if momentum is bearish and trend weak
      - Risk must match cash and portfolio exposure

    Portfolio:
    {json.dumps(portfolio, indent=2)}

    Cash Available: ₹{cash_available}

    Analysis:
    {json.dumps(analysis, indent=2)}

    Return only valid JSON like:
    {{
      "decisions": [
        {{"symbol": "RELIANCE", "action": "BUY", "quantity": 5}},
        {{"symbol": "TCS", "action": "SELL", "quantity": 2}}
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




