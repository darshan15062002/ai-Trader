# api.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

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