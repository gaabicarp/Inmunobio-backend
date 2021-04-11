from db import dbMongo

class FuenteExperimental(Document):
    id_fuenteExperimental = SequenceField()
    codigo = StringField(default="")
    especie = StringField()
    sexo = StringField()
    cepa = StringField()
    tipo = StringField()
    descripcion = StringField()