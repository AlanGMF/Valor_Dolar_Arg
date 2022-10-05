from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin:password@mon:27017/"
    )

db = client.dolares
collection_dolarhoy = db["dolarhoy"]
collection_infobae = db["infobae"]