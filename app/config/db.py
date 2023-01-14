from pymongo import MongoClient
from decouple import config

USER = config('USER')
PASSWORD = config('PASSWORD')
CONTAINER_NAME = config('CONTAINER_NAME')
CONTAINER_PORT = config('CONTAINER_PORT')

URL_STR = f"mongodb://{USER}:{PASSWORD}@{CONTAINER_NAME}:{CONTAINER_PORT}/"

client = MongoClient(URL_STR)

db = client.dolares
