# api.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from datetime import datetime
templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to Atlas
client = AsyncIOMotorClient("mongodb+srv://darshan:$$dar$$123@cluster0.ohxhu.mongodb.net/ai-trading?retryWrites=true&w=majority")
db = client["trading_db"]
snapshots_collection = db["agent_snapshots"]

@app.get("/api/agent_snapshots")
async def get_agent_snapshots(agent_name: str = "gemini-flash-2.0"):
    cursor = snapshots_collection.find(
        {"agent_name": agent_name},
        {"_id": 0}  # exclude MongoDB _id
    ).sort("date", 1)  # ascending by date

    snapshots = await cursor.to_list(length=1000)  # adjust as needed

    # Convert date to ISO string for JSON (React compatibility)
    for snap in snapshots:
        if isinstance(snap["date"], datetime):
            snap["date"] = snap["date"].strftime("%Y-%m-%d")
        elif hasattr(snap["date"], "isoformat"):  # if it's a date object
            snap["date"] = snap["date"].isoformat()

    return snapshots

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Fetch all snapshots for the agent
    snapshots = await snapshots_collection.find(
        {"agent_name": "gemini-flash-2.0"},
        {"_id": 0}
    ).sort("date", 1).to_list(length=1000)

    if not snapshots:
        return HTMLResponse("<h1>No data found</h1>")

    # Compute equity and PnL
    processed = []
    starting_balance = snapshots[0].get("total_credits", 1000000)
    prev_equity = starting_balance

    for snap in snapshots:
        portfolio_value = sum(
            asset["quantity"] * asset["buy_price"]
            for asset in snap["portfolio"]
        )
        equity = snap["credits"] + portfolio_value
        pnl = equity - prev_equity
        prev_equity = equity

        processed.append({
            "date": snap["date"],
            "equity": equity,
            "pnl": pnl,
            "credits": snap["credits"],
            "portfolio": snap["portfolio"]
        })

    # Prepare data for template
    dates = [s["date"] for s in processed]
    equities = [s["equity"] for s in processed]
    latest = processed[-1]

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "dates": dates,
            "equities": equities,
            "snapshots": processed,
            "latest_date": latest["date"],
            "latest_portfolio": latest["portfolio"],
            "latest_credits": latest["credits"],
            "latest_equity": latest["equity"]
        }
    )
