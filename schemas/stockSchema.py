from models.mongo.stock import Stock
from marshmallow import Schema, fields, post_load
from schemas.productosEnStockSchema import ProductosEnStockSchema,ModificarProductoEnStock

class StockSchema(Schema):
    id_productoEnStock = fields.Integer()
    id_espacioFisico = fields.Integer()
    id_grupoDeTrabajo = fields.Integer()
    id_producto = fields.Integer()  #se toma de producto
    nombre = fields.String() #se toma de producto
    producto = fields.Nested(ProductosEnStockSchema,many=True)

class NuevoStockSchema(StockSchema):
    id_producto = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_producto", "code": 400}})
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_espacioFisico", "code": 400}})
    id_grupoDeTrabajo = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_grupoDeTrabajo", "code": 400}})

    @post_load
    def makeProductoEnStock(self, data, **kwargs):
        return Stock(**data)

class busquedaStocksSchema(Schema):
    id_productoEnStock = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_productoEnStock", "code": 400}})
    id_productos = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_productos", "code": 400}})

class ModificarProducto(busquedaStocksSchema):
    producto = fields.Nested(ModificarProductoEnStock)