from db import dbMongo
from dateutil import parser
import datetime

class Blog(dbMongo.EmbeddedDocument):
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    detalle = dbMongo.StringField()
    id_usuario = dbMongo.IntField()
    id_blog = dbMongo.SequenceField()
    tipo = dbMongo.StringField()
    #agregar tipo experimento, o jaula 



