from db import dbMongo

class ProductosStock(dbMongo.EmbeddedDocument):
    lote = dbMongo.StringField()
    fechaVencimiento = dbMongo.DateTimeField()
    producto = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductoEnStock'))
    nombre = dbMongo.StringField() #se toma de producto
    id_producto = dbMongo.IntField()  #se toma de producto


class ProductoEnStock(dbMongo.EmbeddedDocument):
    id_espacioFisico = dbMongo.IntField()
    codigoContenedor = dbMongo.IntField() #opcional
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()

   
