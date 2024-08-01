from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
