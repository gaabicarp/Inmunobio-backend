from db import dbMongo
import datetime
from dateutil import parser

class Muestra(dbMongo.Document):
    id_muestra = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    id_grupoExperimental = dbMongo.IntField()
    id_experimento = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
    id_contenedor= dbMongo.IntField()
    habilitada = dbMongo.BooleanField(default=True)
    id_fuenteExperimental = dbMongo.IntField()


