from db import dbMongo
from models.mongo.muestraPropia import MuestraPropia
from models.mongo.fuenteExperimentalPropia import FuenteExperimentalPropia

class GrupoExperimental(dbMongo.Document):
    id_grupoExperimental = dbMongo.SequenceField()
    id_experimento = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    tipo = dbMongo.StringField()
    fuentesExperimentales = dbMongo.ListField(dbMongo.EmbeddedDocumentField(FuenteExperimentalPropia))
    muestras = dbMongo.ListField(dbMongo.EmbeddedDocumentField(MuestraPropia)) #Guardar muestra propias (copia)
    parent = dbMongo.IntField(default = 0)
    habilitado = dbMongo.BooleanField(default = True)

    
