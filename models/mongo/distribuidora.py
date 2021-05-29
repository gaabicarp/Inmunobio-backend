from db import dbMongo

class Distribuidora(dbMongo.Document):
    nombre = dbMongo.StringField()
    direccion = dbMongo.StringField(default="")
    contacto = dbMongo.StringField()
    cuit = dbMongo.StringField(default="")
    representante = dbMongo.StringField(default="")
    id_distribuidora = dbMongo.SequenceField()