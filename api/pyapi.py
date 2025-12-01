import os
import sys
import pymongo
from flask import Flask, request, make_response, jsonify
from marshmallow import Schema, fields
from bson import ObjectId
from pprint import pprint

from candidates_schema import CreateCandidateSchema, UpdateCandidateSchema
from candidates_service import CandidatesService

os.environ['FLASK_ENV'] = 'development'
app = Flask(__name__)

VERSION = 'v1'
BASE_URL = '/api/' + VERSION

def decodeId(obj):
    obj['_id'] = str(obj['_id'])
    return obj

def encodeId(obj):
    obj['_id'] = ObjectId(obj['_id'])
    return obj

# Endpoints --------------------------------------------------------------------

candidates_service = None

# Create a new candidate
@app.route(BASE_URL + '/candidate', methods=['POST'])
def create_candidate():
    global candidates_service

    candidate = request.get_json()
    create_candidate_schema = CreateCandidateSchema()
    errors = create_candidate_schema.validate(candidate)
    if errors:
        return make_response(str(errors), 400)

    candidates_service.create_candidate(candidate)
    decodeId(candidate)
    return jsonify(candidate), 201

# Delete candidate
@app.route(BASE_URL + '/candidate/<candidateId>', methods=['DELETE'])
def delete_candidate(candidateId):
    global candidates_service

    candidates_service.delete_candidate(candidateId)
    return '', 204

# Return all candidates
@app.route(BASE_URL + '/candidates', methods=['GET'])
def get_candidates():
    global candidates_service

    allCandidates = [decodeId(c) for c in candidates_service.get_candidates()]
    return jsonify(allCandidates)

# Return a specific candidate
@app.route(BASE_URL + '/candidate/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    global candidates_service

    candidate = candidates_service.get_candidate(candidate_id)

    if candidate is None:
        return f"candidate_id not found: {candidate_id}", 404

    return decodeId(candidate)

# Update candidate

@app.route(BASE_URL + '/candidate/<candidate_id>', methods=['PATCH'])
def update_candidate(candidate_id):
    global candidates_service

    update_candidate_schema = UpdateCandidateSchema()
    candidate = candidates_service.get_candidate(candidate_id)

    if candidate is None:
        return f"candidate_id not found: {candidate_id}", 404

    candidate_update = request.get_json()
    errors = update_candidate_schema.validate(candidate_update)
    if errors:
        return make_response(str(errors), 400)
    
    candidate.update(candidate_update)

    if candidates_service.update_candidate(encodeId(candidate)):
        return jsonify(decodeId(candidate)), 200
    else:
        return '', 404

# Main -------------------------------------------------------------------------
def main():
    global candidates_service

    db_name = sys.argv[1] if len(sys.argv) > 1 else 'candidatesDB'

    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    candidates_service = CandidatesService(db_name, mongo_client)
    app.run(debug = 'APP_DEBUG' in os.environ)

if __name__ == '__main__':
    main()
