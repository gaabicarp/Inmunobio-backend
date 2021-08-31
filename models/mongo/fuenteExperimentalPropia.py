
from db import dbMongo

class FuenteExperimentalPropia(dbMongo.EmbeddedDocument):
    id_fuenteExperimental = dbMongo.IntField()
    id_proyecto = dbMongo.IntField()
    codigo = dbMongo.StringField()
    codigoGrupoExperimental = dbMongo.StringField()
    especie = dbMongo.StringField()
    sexo = dbMongo.StringField(required=False, missing = "")
    cepa = dbMongo.StringField()
    tipo = dbMongo.StringField()
    baja = dbMongo.BooleanField(required=False, allow_none=True)
    id_jaula = dbMongo.IntField(required=False, allow_none=True)
    descripcion = dbMongo.StringField(required=False, missing = "")
