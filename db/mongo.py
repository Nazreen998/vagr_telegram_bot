# db/mongo.py
import os
from pymongo import MongoClient # type: ignore

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("❌ MONGO_URI not set")

client = MongoClient(MONGO_URI)
db = client["abhinav_bot"]

orders_collection = db["orders"]
