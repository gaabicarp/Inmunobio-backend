from models.mongo.productosStock import ProductosStock,ProductoEnStock
from marshmallow import Schema, fields, post_load, ValidationError

class ProductosStockSchema(Schema):
    lote = fields.String()
    fechaVencimiento = fields.DateTime(null=True)
    nombre = StringField() 
    id_producto = fields.Integer()  
    producto = fields.Nested(ProductoEnStockSchema, many=True)

class NuevoProductosStockSchema(ProductosStockSchema):
    lote = fields.String(required=True, error_messages={"required": {"message" : "Debe indicarse lote", "code": 400}})
    producto = fields.Nested(ProductoNuevoStockSchema)
    @post_load
    def make_Stock(self, data, **kwargs):
        return Stock(**data)
#schemas para productos dentro producto en stock

class ProductoEnStockSchema(Schema):
    id_espacioFisico = fields.Integer()
    codigoContenedor = fields.Integer()
    detalleUbicacion = fields.String(default="")
    unidad = fields.Integer()
    codigoContenedor =  fields.Integer(null=True)

class ProductoNuevoStockSchema(ProductoEnStockSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_espaciofisico", "code": 400}})
  


    