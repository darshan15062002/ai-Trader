from ReportEngine.agent import ReportAgent
import os

# Set your Gemini API key
os.environ["GEMINI_API_KEY"] = "AIzaSyAfjsA-tRRq6iBmlvX1abOmZgIDweq_Hwg"

# Create test data
test_data = {
    "summary": "Stock market analysis shows positive trends with technology sector leading gains",
    "sentiment_analysis": "Bullish sentiment at 65%, bearish at 25%, neutral at 10%",
    "key_insights": [
        "Strong earnings in semiconductor sector",
        "Increased retail investor participation",
        "Regulatory concerns in fintech space"
    ],
    "recommendations": [
        "Consider dollar-cost averaging for volatile stocks",
        "Diversify across sectors to mitigate risk",
        "Monitor Federal Reserve announcements closely"
    ]
}

# Generate report
agent = ReportAgent()
report_path = agent._generate_html_report(
    forum_log=None,
    agent_outputs=test_data
)

print(f"Report generated successfully at: {report_path}")