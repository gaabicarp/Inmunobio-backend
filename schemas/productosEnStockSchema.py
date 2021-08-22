from models.mongo.productosEnStock import ProductosEnStock
from marshmallow import Schema, fields, post_load
from models.mongo.validacion import Validacion

class IdProductosEnStockSchema(Schema):
    id_productos =  fields.Integer(required=True,validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Debe indicarse id_productos", "code": 400}})

class ModificarProductoEnStock(IdProductosEnStockSchema):
    codigoContenedor = fields.Integer()
    detalleUbicacion = fields.String()

class ProductoEnStockSchema(ModificarProductoEnStock):
    id_productos =  fields.Integer()
    lote = fields.String(default="")
    fechaVencimiento = fields.DateTime()
    unidad = fields.Integer()

class NuevoProductoEnStockSchema(ProductoEnStockSchema):
    unidad = fields.Integer(required=True,validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Deben indicarse unidades", "code": 400}})
    @post_load
    def makeProductos(self, data, **kwargs):
        return ProductosEnStock(**data)

