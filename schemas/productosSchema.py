from models.mongo.productos import Productos
from marshmallow import Schema, fields, post_load

class IdProductosSchema(Schema):
    id_productos =  fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_productos", "code": 400}})

class ProductosSchema(Schema):
    id_productos =  fields.Integer(dump_only=True)
    codigoContenedor = fields.Integer()
    detalleUbicacion = fields.String(default="")
    unidad =fields.Integer(default=0)
    lote = fields.String(default="")
    fechaVencimiento = fields.DateTime()

class NuevoProductosSchema(ProductosSchema):
    unidad = fields.Integer(required=True, error_messages={"required": {"message" : "Deben indicarse unidades", "code": 400}})
    @post_load
    def makeProductos(self, data, **kwargs):
        return Productos(**data)