from marshmallow import Schema, fields, post_load
from models.mongo.distribuidora import Distribuidora
from models.mongo.validacion import Validacion


class DistribuidoraSchema(Schema):
    nombre = fields.String()
    direccion = fields.String()
    contacto = fields.String()
    cuit = fields.String()
    representante = fields.String()
    id_distribuidora = fields.Integer(dump_only=True)

class ModificarDistribuidora(DistribuidoraSchema):
    id_distribuidora = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse id_distribuidora", "code": 400}}) 

class NuevaDistribuidoraSchema(DistribuidoraSchema):
    nombre = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse nombre de distribuidora", "code": 400}}) 
    contacto = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse contacto", "code": 400}}) 
    
    @post_load
    def makeDistribuidora(self, data, **kwargs):
        return Distribuidora(**data)

