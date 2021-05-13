from db import dbMongo
from models.mongo.productos import Productos

class ProductoEnStock(dbMongo.EmbeddedDocument):
    id_productoEnStock =  dbMongo.SequenceField()
    nombre = dbMongo.StringField() #se toma de producto
    id_producto = dbMongo.IntField()  #se toma de producto
    productos = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Productos'))
    #TO-DO:unidades totales puede ser calculado ver
  

