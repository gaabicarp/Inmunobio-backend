from db import dbMongo
import datetime
from bson import ObjectId
from dateutil import parser
 
class Proyecto(dbMongo.Document):

    id_proyecto = dbMongo.SequenceField()
    codigoProyecto = dbMongo.StringField()
    nombre = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFinal = dbMongo.DateTimeField()
    finalizado = dbMongo.BooleanField(default=False)
    montoInicial = dbMongo.DecimalField()
    conclusion = dbMongo.StringField()
    participantes = dbMongo.ListField(dbMongo.IntField())
    idDirectorProyecto = dbMongo.IntField()

