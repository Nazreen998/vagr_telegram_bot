# db/mongo.py
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not set")

_client = None

def get_orders_collection():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
    db = _client["telegram_bot"]   # ✅ matches Atlas
    return db["orders"]
