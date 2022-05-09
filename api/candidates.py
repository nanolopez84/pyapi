import pymongo
from bson import ObjectId
from pprint import pprint

db      = None  # Name convention avoided
gClient = None
gName   = None

def createCandidate(candidate):
    global db
    db.candidates.insert_one(candidate)
    return candidate

def deleteCandidate(candidateId):
    global db
    db.candidates.delete_one({'_id': candidateId})

def dropDatabase():
    global gClient
    global gName
    gClient.drop_database(gName)

def getCandidates():
    global db
    return list(db.candidates.find())

def init(name='candidatesDB'): # pragma: no cover
    global db
    global gClient
    global gName

    gName = name
    gClient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = gClient[gName]
    db.candidates.drop()

def updateCandidate(candidate):
    global db
    res = db.candidates.update_one({'_id': candidate['_id']}, {'$set': candidate})

    # Do not mind if data was modified, just evaluate matched _id
    return res.matched_count == 1
