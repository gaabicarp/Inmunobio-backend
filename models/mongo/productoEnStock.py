from db import dbMongo

class ProductoEnStock(dbMongo.EmbeddedDocument):
    id_productoEnStock =  dbMongo.SequenceField()
    id_espacioFisico = dbMongo.IntField()
    codigoContenedor = dbMongo.IntField() #opcional
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()

