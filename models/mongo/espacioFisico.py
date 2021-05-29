from db import dbMongo
from models.mongo.blog import Blog

class EspacioFisico(dbMongo.Document):
    nombre = dbMongo.StringField()
    piso = dbMongo.StringField()
    sala = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Blog'))
    tipo = dbMongo.StringField() #Revisar y preguntar /Taller, Bioterio, etc
    herramientas = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Herramienta'))
    jaulas = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Jaula'))
    