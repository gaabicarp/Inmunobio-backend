from db import dbMongo
import datetime
from dateutil import parser
from models.mongo.muestraExterna import MuestraExterna

class Experimento(dbMongo.Document):
    id_experimento = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    codigo = dbMongo.StringField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFin = dbMongo.DateTimeField()
    resultados = dbMongo.StringField(default="")
    finalizado = dbMongo.BooleanField(default=False)
    metodologia = dbMongo.StringField()
    conclusiones = dbMongo.StringField(default="")
    objetivos = dbMongo.StringField()
    muestrasExternas = dbMongo.ListField(dbMongo.EmbeddedDocumentField('MuestraExterna'))
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Blog'))

    

