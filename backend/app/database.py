from pymongo import MongoClient

client = MongoClient("mongodb+srv://sourabhchoudhari0123_db_user:YOUR_PASSWORD@cluster0.svlnrxn.mongodb.net/finance_tracker")

db = client["finance_tracker"]

users_collection = db["users"]
transactions_collection = db["transactions"]