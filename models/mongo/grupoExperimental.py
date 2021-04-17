from db import dbMongo

class GrupoExperimental(Document):
    id_grupoExperimental = SequenceField()
    codigo = StringField()
    descripcion = StringField()
    tipo = StringField()
    fuentesExperimentales = IntegerListField()
    muestras = IntegerListField()
    parent = IntegerField(default = 0)
    habilitado = BooleanField(default = False)