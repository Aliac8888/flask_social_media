from urllib.parse import quote_plus
from pymongo import MongoClient
from config import db_user, db_pass, db_host, db_port

USER_NOT_FOUND = 11
DUPLICATE_KEY = 11000

client = MongoClient(
    f"mongodb://{quote_plus(db_user)}:{quote_plus(db_pass)}@{db_host}:{db_port}/"
)

db = client["social_media"]
