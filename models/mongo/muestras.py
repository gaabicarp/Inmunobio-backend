from db import dbMongo

class Muestras(Document):
    codigo = StringField()
    nombre = StringField()
    fecha = dateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = StringField()
    id_contenedor= IntegerField()