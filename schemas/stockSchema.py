from models.mongo.stock import Stock
from marshmallow import Schema, fields, post_load, ValidationError
from schemas.productoEnStockSchema import ProductoEnStockSchema,NuevoProductoEnStockSchema

class StockSchema(Schema):
    lote = fields.String()
    fechaVencimiento = fields.DateTime(null=True)
    nombre = fields.String()
    id_producto = fields.Integer()  
    producto = fields.Nested(ProductoEnStockSchema, many=True)  
      
class NuevoStockSchema(StockSchema):
    lote = fields.String(required=True, error_messages={"required": {"message" : "Debe indicarse lote", "code": 400}})
    id_producto = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_producto", "code": 400}}) 
    producto = fields.Nested(NuevoProductoEnStockSchema, many=True) 
    @post_load
    def make_Stock(self, data, **kwargs):
        return Stock(**data)



  


