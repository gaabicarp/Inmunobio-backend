from db import dbMongo

class Blog(EmbeddedDocument):
    fecha = DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    detalle = StringField()
    id_usuario = IntField()