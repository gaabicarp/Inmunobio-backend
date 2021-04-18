from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from flask import jsonify




class Stock(dbMongo.EmbeddedDocument):
    lote = dbMongo.StringField()#Charlar stock y lote
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()
    fechaVencimiento = dbMongo.DateTimeField()
    id_espacioFisico = dbMongo.IntField()
    codigoContenedor = dbMongo.StringField() 

class StockSchema(Schema):
    lote = fields.Integer()
    detalleUbicacion = fields.String()
    unidad = fields.Integer()
    fechaVencimiento = fields.DateTime()
    id_espacioFisico = fields.Integer()
    codigoContenedor =  fields.String()