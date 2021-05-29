from db import dbMongo
from models.mongo.stock import Stock

class GrupoDeTrabajo(dbMongo.Document):
    id_grupoDeTrabajo = dbMongo.SequenceField()
    nombre = dbMongo.StringField()
    jefeDeGrupo = dbMongo.IntField()
    integrantes = dbMongo.ListField(dbMongo.IntField()) #ver duplicados en integrantes
    #stock = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Stock'))
    grupoGral = dbMongo.BooleanField(default=False)

