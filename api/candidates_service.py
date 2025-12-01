import pymongo
from bson import ObjectId
from pprint import pprint

class CandidatesService:
    def __init__(self, name, client):
        self._name = name
        self._client = client
        self._db = self._client[self._name]

    def create_candidate(self, candidate):
        self._db.candidates.insert_one(candidate)
        return candidate

    def delete_candidate(self, candidate_id):
        self._db.candidates.delete_one({'_id': ObjectId(candidate_id)})

    def drop_database(self):
        self._client.drop_database(self._name)

    def get_candidates(self):
        return list(self._db.candidates.find())

    def get_candidate(self, candidate_id):
        return self._db.candidates.find_one({'_id': ObjectId(candidate_id)})

    def update_candidate(self, candidate):
        res = self._db.candidates.update_one({'_id': candidate['_id']}, {'$set': candidate})
        return res.matched_count == 1
