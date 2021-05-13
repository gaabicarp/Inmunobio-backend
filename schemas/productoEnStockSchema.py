from models.mongo.productoEnStock import ProductoEnStock
from marshmallow import Schema, fields, post_load
from schemas.productoSchema import ProductosSchema

class ProductoEnStockSchema(Schema):
    id_productoEnStock = fields.Integer()
    id_producto = fields.Integer()  #se toma de producto
    nombre = fields.String() #se toma de producto
    productos = fields.Nested(ProductosSchema,many=True)
    
class NuevoProductoEnStockSchema(ProductoEnStockSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_espaciofisico", "code": 400}})
    @post_load
    def makeProductoEnStock(self, data, **kwargs):
        return ProductoEnStock(**data)

