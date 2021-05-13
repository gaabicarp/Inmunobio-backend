from models.mongo.stock import Stock
from marshmallow import Schema, fields, post_load
from schemas.productoEnStockSchema import ProductoEnStockSchema

class StockSchema(Schema):
    id_espacioFisico = fields.Integer()  
    producto = fields.Nested(ProductoEnStockSchema, many=True)  
      
class NuevoStockSchema(StockSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse lote", "code": 400}})
    @post_load
    def make_Stock(self, data, **kwargs):
        return Stock(**data)







  


