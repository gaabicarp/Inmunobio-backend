from db import dbMongo
from models.mongo.jaula import Jaula

class EspacioFisico(dbMongo.Document):
    nombre = dbMongo.StringField()
    piso = dbMongo.StringField()
    sala = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Blog'))
    id_espacioFisico = dbMongo.SequenceField()
    #tipo = dbMongo.StringField() #Revisar y preguntar /Taller, Bioterio, etc
