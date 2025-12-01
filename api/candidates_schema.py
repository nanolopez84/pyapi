from marshmallow import Schema, fields

class CreateCandidateSchema(Schema):
    name = fields.Str(required=True)
    age  = fields.Int(required=True)

class UpdateCandidateSchema(Schema):
    name = fields.Str(required=False)
    age  = fields.Int(required=False)
