
from models.mongo.producto import Producto
from marshmallow import Schema, fields, post_load
from models.mongo.validacion import Validacion

class IdProductoSchema(Schema):
    id_producto = fields.Integer(required=True,validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Debe indicarse el id de producto", "code": 400}})

class ModificarProductoSchema(IdProductoSchema):
    url = fields.String()
    aka =  fields.String()
    tipo =  fields.String()
    detallesTecnicos =  fields.String()#Se sube archivo .txt
    protocolo = fields.String() #Se sube archivo
    id_distribuidora =  fields.Integer()
    marca =  fields.String()
    nombre = fields.String()
    unidadAgrupacion =  fields.Integer(default=1)
    id_producto = fields.Integer()

class ProductoSchema(ModificarProductoSchema):
    id_producto = fields.Integer(dump_only=True)
    #unidadAgrupacion =  fields.Integer(default=1)

class NuevoProductoSchema(ProductoSchema):
    nombre = fields.String(required=True,validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Debe indicarse el nombre de producto", "code": 400}})
    marca =  fields.String(required=True,validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Debe indicarse la marca del producto", "code": 400}})

    @post_load
    def makeProducto(self, data, **kwargs):
        return Producto(**data)