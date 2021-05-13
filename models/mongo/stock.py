from db import dbMongo
from models.mongo.productoEnStock import ProductoEnStock

class Stock(dbMongo.EmbeddedDocument):
    productos = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductoEnStock'))
    id_espacioFisico = dbMongo.IntField()




   
