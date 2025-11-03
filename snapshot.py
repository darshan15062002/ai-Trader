# trading_script.py
from pymongo import MongoClient
from datetime import date

# Replace with your Atlas connection string
MONGO_URI = "mongodb+srv://darshan:$$dar$$123@cluster0.ohxhu.mongodb.net/ai-trading?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["trading_db"]
snapshots_collection = db["agent_snapshots"]




def save_agent_snapshot(agent_data, snapshot_date=None):
    if snapshot_date is None:
        snapshot_date = date.today()
    
    # Convert to ISO string: "2025-11-03"
    date_str = snapshot_date.isoformat()  # works for date or datetime

    snapshot = {
        **agent_data,
        "date": date_str,  # ✅ string is always safe
        "agent_name": agent_data["name"]
    }

    snapshots_collection.update_one(
        {"agent_name": agent_data["name"], "date": date_str},
        {"$set": snapshot},
        upsert=True
    )
