import os
import pymongo


username = os.environ.get("DB_ACCESS_USERNAME")
password = os.environ.get("DB_ACCESS_PASSWORD")
db_name = "fishyBot"
registered_user_collection = "Registered Users"
analysis_board_collection = "Analysis Boards"
banned_user_collection = "Banned Users"
games_collection = "Game Archives"


conn_str = f"mongodb+srv://{username}:{password}@faltu-projects.m6hhn.mongodb.net/"

def setup_db_collection(db,collection):
    db_client = pymongo.MongoClient(conn_str)
    db = db_client[db]
    col = db[collection]
    return col

def setup_db(db):
    db_client = pymongo.MongoClient(conn_str)
    db = db_client[db]
    return db
