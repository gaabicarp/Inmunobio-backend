from db import dbMongo
from models.mongo.blog import Blog

class Jaula(dbMongo.Document):
    id_jaula = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField(default=0)
    nombre_proyecto = dbMongo.StringField(default="") 
    id_espacioFisico = dbMongo.IntField()#
    codigo = dbMongo.StringField()
    rack = dbMongo.IntField()#
    estante = dbMongo.IntField()#
    tipo = dbMongo.StringField()
    capacidad = dbMongo.IntField()
    habilitado = dbMongo.BooleanField(default = True)
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Blog'))

