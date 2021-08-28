from db import dbMongo
from dateutil import parser
import datetime

class MuestraPropia(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    nombre = dbMongo.StringField()
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
    id_fuenteExperimental = dbMongo.IntField()
