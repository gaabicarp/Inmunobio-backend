from re import I
from db import dbMongo

class FuenteExperimental(dbMongo.Document):
    id_fuenteExperimental = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    codigo = dbMongo.StringField(default="")
    codigoGrupoExperimental = dbMongo.StringField(default="") #Se usa como flag para saber si está disponible
    especie = dbMongo.StringField()
    sexo = dbMongo.StringField()
    cepa = dbMongo.StringField()
    tipo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    id_jaula = dbMongo.IntField()
    baja = dbMongo.BooleanField(default=False)

