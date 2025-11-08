from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["plate_donor"] #databasename

#collection
donations_collection = db["donations"]
users_collection = db["users"]

try:
    print("✅ Connected to:", client.list_database_names())
except Exception as e:
    print("❌ MongoDB Connection Error:", e)




