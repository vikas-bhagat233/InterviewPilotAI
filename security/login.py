import os
from pymongo import MongoClient
from security.auth import hash_password, verify_password

def get_db():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    return client.interviewpilot_db

def register_user(name, email, password):
    db = get_db()
    
    # Ensure email is unique
    if db.users.find_one({"email": email}):
        return False
        
    user = {
        "name": name,
        "email": email,
        "password": hash_password(password)
    }
    
    try:
        db.users.insert_one(user)
        return True
    except:
        return False

def login_user(email, password):
    db = get_db()
    user = db.users.find_one({"email": email})
    
    if user:
        return verify_password(password, user["password"])
    return False