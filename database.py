from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv

if "--test" in sys.argv:
    load_dotenv(override=True)

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DOMAIN = os.getenv("MONGO_DOMAIN")
MONGO_PORT = os.getenv("MONGO_PORT")

URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_DOMAIN}{MONGO_PORT}"
print("URL IS " + URL)

client = MongoClient(URL)

def testDatabaseConnection():
    try:
        client.admin.command('ismaster')
        print("Database connection was successful")
        return True
    except:
        print("Database connection failed")
        return False
    

def getIdeasCollection():
    try:
        return client["list"]["ideas"]
    except:
        return None

def docToDict(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def docsToArray(docs):
    return [docToDict(doc) for doc in docs]