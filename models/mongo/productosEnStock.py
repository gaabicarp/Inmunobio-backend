from db import dbMongo

class ProductosEnStock(dbMongo.EmbeddedDocument):
    id_productos =  dbMongo.SequenceField()
    codigoContenedor = dbMongo.IntField() #opcional
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()
    lote = dbMongo.StringField()
    fechaVencimiento = dbMongo.DateTimeField()



