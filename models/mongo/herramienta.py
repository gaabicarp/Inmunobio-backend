from db import dbMongo

class Herramienta(dbMongo.Document):
    nombre = dbMongo.StringField()
    detalle = dbMongo.StringField()
    id_herramienta = dbMongo.SequenceField()
    id_espacioFisico = dbMongo.IntField()
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Blog'))




