from db import dbMongo
from models.mongo.productosEnStock import ProductosEnStock

class Stock(dbMongo.Document):
    id_productoEnStock =  dbMongo.SequenceField()
    nombre = dbMongo.StringField() #se toma de producto
    id_producto = dbMongo.IntField()  #se toma de producto
    id_espacioFisico = dbMongo.IntField()
    id_grupoDeTrabajo = dbMongo.IntField()
    producto = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductosEnStock'))
    seguimiento = dbMongo.BooleanField()

  

