from db import dbMongo
from flask import jsonify
from models.mongo.productosStock import ProductosStock

class GrupoDeTrabajo(dbMongo.Document):
    id_grupoDeTrabajo = dbMongo.SequenceField()
    nombre = dbMongo.StringField()
    jefeDeGrupo = dbMongo.IntField()
    integrantes = dbMongo.ListField(dbMongo.IntField()) #ver duplicados en integrantes
    stock = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductosStock'))
    grupoGral = dbMongo.BooleanField(default=False)

