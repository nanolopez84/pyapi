import os
from flask import Flask, request, make_response, jsonify
from marshmallow import Schema, fields
from bson import ObjectId
from pprint import pprint

import candidates

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

# Create a new candidate
class CreateCandidateSchema(Schema):
    name = fields.Str(required=True)

createCandidateSchema = CreateCandidateSchema()

@app.route(BASE_URL + '/candidate', methods=['POST'])
def createCandidate():
    errors = createCandidateSchema.validate(request.json)
    if errors:
        return make_response(str(errors), 400)

    candidate = request.json
    candidates.createCandidate(candidate)
    decodeId(candidate)
    return jsonify(candidate), 201

# Delete candidate
@app.route(BASE_URL + '/candidate/<candidateId>', methods=['DELETE'])
def deleteCandidate(candidateId):
    candidates.deleteCandidate(ObjectId(candidateId))
    return '', 204

# Return all candidates
@app.route(BASE_URL + '/candidates', methods=['GET'])
def getCandidates():
    allCandidates = [decodeId(c) for c in candidates.getCandidates()]
    return jsonify(allCandidates)

# Update candidate
class UpdateCandidateSchema(Schema):
    _id     = fields.Str(required=True)
    name    = fields.Str(required=True)

updateCandidateSchema = UpdateCandidateSchema()

@app.route(BASE_URL + '/candidate/<candidateId>', methods=['PATCH'])
def updateCandidate(candidateId):
    errors = updateCandidateSchema.validate(request.json)
    if errors:
        return make_response(str(errors), 400)

    candidate = request.json
    if candidates.updateCandidate(encodeId(candidate)):
        return jsonify(decodeId(candidate)), 200
    else:
        return '', 404

# Main -------------------------------------------------------------------------
try:
    candidates.init()
    app.run(debug = 'APP_DEBUG' in os.environ)
except Exception as e:
    print(e)
finally:
    candidates.close()

