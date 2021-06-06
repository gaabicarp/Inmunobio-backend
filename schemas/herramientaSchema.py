from db import dbMongo
from marshmallow import Schema, fields, post_load
from models.mongo.jaula import Jaula
from schemas.blogSchema import BlogSchema

class HerramientaSchema(dbMongo.Document):
    nombre = fields
    detalle = dbMongo.StringField()
    id_herramienta = dbMongo.IntField()




