from pymongo import MongoClient

client = MongoClient(
        host = "mongodb://localhost:27017/",
        serverSelectionTimeoutMS = 30000, # 3 second timeout
        username = "admin",
        password = "password",
    )