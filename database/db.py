import os
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

def get_db():
    # Fetches from environment, defaults to local for testing
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    return client.interviewpilot_db

def create_tables():
    # MongoDB is NoSQL and creates collections dynamically, so this can pass.
    pass

def save_report(email, score):
    db = get_db()
    report = {
        "email": email,
        "resume_score": score,
        "created_at": datetime.utcnow()
    }
    db.reports.insert_one(report)

def get_user_reports(email):
    db = get_db()
    # Find user reports and sort by newest first
    reports = db.reports.find({"email": email}).sort("created_at", -1)
    
    formatted_reports = []
    for r in reports:
        # app.py expects a tuple: (id, email, score, created_at)
        formatted_reports.append((
            str(r["_id"]), 
            r["email"], 
            r["resume_score"], 
            r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        ))
    return formatted_reports

def get_total_reports():
    db = get_db()
    return db.reports.count_documents({})

def get_all_reports():
    db = get_db()
    return list(db.reports.find().sort("created_at", -1))

def delete_report(report_id):
    db = get_db()
    db.reports.delete_one({"_id": ObjectId(report_id)})