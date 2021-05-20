from marshmallow import Schema, fields, post_load, ValidationError
from models.mongo.distribuidora import Distribuidora

class IdDistribuidoraSchema(Schema):
    id_distribuidora = fields.Integer(required=True,error_messages={"required": {"message": "Debe indicarse id_distribuidora", "code": 400}}) 


class DistribuidoraSchema(Schema):
    nombre = fields.String()
    direccion = fields.String()
    contacto = fields.String()
    cuit = fields.String()
    representante = fields.String()
    id_distribuidora = fields.Integer()

class NuevaDistribuidoraSchema(DistribuidoraSchema):
    nombre = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse nombre de distribuidora", "code": 400}}) 
    contacto = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse contacto", "code": 400}}) 
    @post_load
    def makeDistribuidora(self, data, **kwargs):
        return Distribuidora(**data)