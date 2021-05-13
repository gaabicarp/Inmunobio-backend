from db import dbMongo

class Distribuidora(dbMongo.Document):
    nombre = dbMongo.StringField()
    direccion = dbMongo.StringField()
    contacto = dbMongo.StringField()
    cuit = dbMongo.StringField()
    representante = dbMongo.StringField()
    id_distribuidora = dbMongo.SequenceField()