from db import dbMongo

class MuestraExterna(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.IntField()
    codigo = dbMongo.StringField()
    fecha = dbMongo.DateTimeField()
    tipo = dbMongo.StringField()
    id_proyecto = dbMongo.IntField()
    id_grupoExperimental = dbMongo.IntField()
    id_experimento = dbMongo.IntField()
    descripcion = dbMongo.StringField()
    id_contenedor= dbMongo.IntField()
    habilitada = dbMongo.BooleanField(default=True)
    id_fuenteExperimental =  dbMongo.IntField()
