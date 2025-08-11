from marshmallow import fields, Schema

class BookSchema(Schema):
    id = fields.Int(dump_only = True)
    title = fields.String(required=True)
    author = fields.String(required=True)