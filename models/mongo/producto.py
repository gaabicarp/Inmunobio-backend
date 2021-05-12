from db import dbMongo

class Producto(dbMongo.Document):
    nombre = dbMongo.StringField()
    tipo = dbMongo.StringField()
    aka = dbMongo.StringField()
    marca = dbMongo.StringField()
    url = dbMongo.StringField()
    unidadAgrupacion = dbMongo.IntField()
    detallesTecnicos = dbMongo.StringField() #Se sube archivo .txt
    protocolo = dbMongo.StringField() #Se sube archivo
    id_distribuidora = dbMongo.IntField()
    id_producto = dbMongo.SequenceField()
