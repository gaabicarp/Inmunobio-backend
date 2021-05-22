from db import dbMongo
from dateutil import parser
from marshmallow import Schema, fields, post_load
import datetime

class Blog(dbMongo.EmbeddedDocument):
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    detalle = dbMongo.StringField()
    id_usuario = dbMongo.IntField()

    def json(self):
        return BlogSchema.dump(self)

class BlogSchema(Schema):
    fecha = fields.DateTime()
    detalle = fields.Str()
    id_usuario = fields.Int()