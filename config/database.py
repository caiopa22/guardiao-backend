from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CLIENT=os.getenv("MONGO_CLIENT")

if not MONGO_CLIENT:
    raise ValueError("No MONGO_CLIENT environment variable set")

client = MongoClient(MONGO_CLIENT)
db = client.guardiao

users_collection = db['users']
users_collection.create_index("email", unique=True)