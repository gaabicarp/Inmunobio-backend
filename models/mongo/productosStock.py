from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from flask import jsonify

class ProductosStock(dbMongo.EmbeddedDocument):
    lote = dbMongo.StringField()
    fechaVencimiento = dbMongo.DateTimeField()
    producto = dbMongo.ListField(dbMongo.EmbeddedDocumentField('ProductoEnStock')))
    nombre = StringField() #se toma de producto
    id_producto = dbMongo.IntField()  #se toma de producto

class ProductosStockSchema(Schema):
    lote = fields.String()
    fechaVencimiento = fields.DateTime(null=True)
    nombre = StringField() 
    id_producto = fields.Integer()  
    producto = fields.Nested(ProductoEnStockSchema, many=True)

class NuevoProductosStockSchema(ProductosStockSchema):
    lote = fields.String(required=True, error_messages={"required": {"message" : "Debe indicarse lote", "code": 400}})
    producto = fields.Nested(ProductoNuevoStockSchema)
    @post_load
    def make_Stock(self, data, **kwargs):
        return Stock(**data)