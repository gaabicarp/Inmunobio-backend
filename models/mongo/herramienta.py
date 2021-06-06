from db import dbMongo
from dateutil import parser
import datetime

class Herramienta(dbMongo.Document):
    nombre = dbMongo.StringField()
    detalle = dbMongo.StringField()
    id_herramienta = dbMongo.SequenceField()
    id_espacioFisico = dbMongo.IntField()




