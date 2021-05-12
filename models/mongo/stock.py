from db import dbMongo
from models.mongo.productoEnStock import ProductoEnStock

class Stock(dbMongo.EmbeddedDocument):
    lote = dbMongo.StringField()
    fechaVencimiento = dbMongo.DateTimeField()
    producto = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductoEnStock'))
    nombre = dbMongo.StringField() #se toma de producto
    id_producto = dbMongo.IntField()  #se toma de producto
    id_stock =  dbMongo.SequenceField()



   
