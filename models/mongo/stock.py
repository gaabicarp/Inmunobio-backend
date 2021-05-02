from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from flask import jsonify

class producto(dbMongo.EmbeddedDocument):
#esto seria producto
    lote = dbMongo.StringField()
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()
    fechaVencimiento = dbMongo.DateTimeField()
    id_espacioFisico = dbMongo.IntField()
    codigoContenedor = dbMongo.IntField() #opcional
    #id producto falta  

class NuevoStockSchema(Schema):
    lote = fields.String(required=True, error_messages={"required": {"message" : "Debe indicarse lote", "code": 400}})
    detalleUbicacion = fields.String(default="")
    unidad = fields.Integer(default=1)
    fechaVencimiento = fields.DateTime(null=True)
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_espaciofisico", "code": 400}})
    codigoContenedor =  fields.Integer(null=True)
    
    @post_load
    def make_Stock(self, data, **kwargs):
        return Stock(**data)

class StockSchema(Schema):
    lote = fields.String()
    detalleUbicacion = fields.String()
    unidad = fields.Integer()
    fechaVencimiento = fields.DateTime()
    id_espacioFisico = fields.Integer()
    codigoContenedor =  fields.Integer()
