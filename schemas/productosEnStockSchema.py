from models.mongo.productosEnStock import ProductosEnStock
from marshmallow import Schema, fields, post_load

class IdProductosEnStockSchema(Schema):
    id_productos =  fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_productos", "code": 400}})

class ModificarProductoEnStock(Schema):
    codigoContenedor = fields.Integer()
    detalleUbicacion = fields.String()
    unidad =fields.Integer()

class ProductosEnStockSchema(ModificarProductoEnStock):
    id_productos =  fields.Integer(dump_only=True)
    lote = fields.String(default="")
    fechaVencimiento = fields.DateTime()

class NuevoProductosEnStockSchema(ProductosEnStockSchema):
    unidad = fields.Integer(required=True, error_messages={"required": {"message" : "Deben indicarse unidades", "code": 400}})
    @post_load
    def makeProductos(self, data, **kwargs):
        return ProductosEnStock(**data)

