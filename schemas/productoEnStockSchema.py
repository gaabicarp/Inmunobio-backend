from models.mongo.productoEnStock import ProductoEnStock
from marshmallow import Schema, fields, post_load, ValidationError

class ProductoEnStockSchema(Schema):
    id_espacioFisico = fields.Integer()
    codigoContenedor = fields.Integer()
    detalleUbicacion = fields.String(default="")
    unidad = fields.Integer(default=1)
    #codigoContenedor =  fields.Integer(null=True)

class NuevoProductoEnStockSchema(ProductoEnStockSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_espaciofisico", "code": 400}})
    @post_load
    def make_ProductoEnStock(self, data, **kwargs):
        return ProductoEnStock(**data)