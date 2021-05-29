from db import dbMongo

class Blog(dbMongo.EmbeddedDocument):
    fecha = DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    detalle = StringField()
    id_usuario = IntField()