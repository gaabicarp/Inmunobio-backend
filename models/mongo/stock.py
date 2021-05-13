from db import dbMongo
from models.mongo.productoEnStock import ProductoEnStock

class Stock(dbMongo.EmbeddedDocument):
    producto = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductoEnStock'))
    id_espacioFisico = dbMongo.IntField()




   
