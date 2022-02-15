from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(f"mongodb+srv://admin:{os.getenv('password')}@cluster0.a5y3r.mongodb.net/Banana_Bot?retryWrites=true&w=majority")
db = client.Banana_Bot

def get_user(id):
    return db.users.find_one({"_id": id})

def create_user(id):
    db.users.insert_one({
        "_id": id,
        "social_credit": 0,
        "warns": []
    })

def delete_user(id):
    db.users.delete_one({
        "_id": id
    })

def reset_credits(id):
    db.users.update_one({
        "_id": id
    }, {
        "$set": {
            "social_credit": 0
        }
    })

def add_credits(id, credits):
    db.users.update_one({
        "_id": id
    }, {
        "$inc": {
            "social_credit": credits
        }
    })

def sub_credits(id, credits):
    db.users.update_one({
        "_id": id
    }, {
        "$inc": {
            "social_credit": -credits
        }
    })

def set_credits(id, credits):
    db.users.update_one({
        "_id": id
    }, {
        "$set": {
            "social_credit": credits
        }
    })

def reset_warns(id):
    db.users.update_one({
        "_id": id
    }, {
        "$set": {
            "warns": []
        }
    })

def add_warn(id, warn):
    db.users.update_one({
        "_id": id
    }, {
        "$push": {
            "warns": warn
        }
    })

def add_point(phrase, status):
    db.dataset.insert_one({"type": status, "phrase": phrase})

def get_dataset():
    good = [point["phrase"] for point in db.dataset.find({"type": "good"})]
    bad = [point["phrase"] for point in db.dataset.find({"type": "bad"})]
    neutral = [point["phrase"] for point in db.dataset.find({"type": "neutral"})]
    return {"good": good, "bad": bad, "neutral": neutral}
