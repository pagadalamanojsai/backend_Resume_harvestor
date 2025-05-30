import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import MONGO_URI


from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.get_default_database()

def save_candidate(candidate_dict):
    return db.candidates.insert_one(candidate_dict)

def get_candidates(query=None):
    if query is None:
        query = {}
    return list(db.candidates.find(query))

def get_candidate_by_id(candidate_id):
    from bson.objectid import ObjectId
    return db.candidates.find_one({'_id': ObjectId(candidate_id)})

