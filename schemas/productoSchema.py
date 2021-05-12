
from marshmallow import Schema, fields, post_load, ValidationError

class IdProductoSchema(Schema):
    id_producto = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse el id de producto", "code": 400}})

    
class ProductoSchema(Schema):
    nombre = fields.String()
    tipo =  fields.String()
    aka =  fields.String()
    marca =  fields.String()
    url = fields.String()
    unidadAgrupacion =  fields.Integer(default=1)
    detallesTecnicos =  fields.String()#Se sube archivo .txt
    protocolo = fields.String() #Se sube archivo
    id_distribuidora =  fields.Integer()
    id_producto = fields.Integer()

class NuevoProductoSchema(ProductoSchema):
    nombre = fields.String(required=True, error_messages={"required": {"message" : "Debe indicarse el nombre de producto", "code": 400}})
    marca =  fields.String(required=True, error_messages={"required": {"message" : "Debe indicarse la marca del producto", "code": 400}})
    id_distribuidora =  fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse el id de distribuidora", "code": 400}})
