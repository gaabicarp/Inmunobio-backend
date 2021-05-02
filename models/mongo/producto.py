from marshmallow import Schema, fields, post_load, ValidationError


class Producto(Document):
    nombre = StringField()
    tipo = StringField()
    aka = StringField()
    marca = StringField()
    url = StringField()
    unidadAgrupacion = StringField()
    detallesTecnicos = StringField() #Se sube archivo .txt
    protocolo = StringField() #Se sube archivo
    id_distribuidora = ReferenciasField(required=True)
    id_producto = SequenceField()

class ProductoEnStock(dbMongo.EmbeddedDocument):
    id_espacioFisico = dbMongo.IntField()
    codigoContenedor = dbMongo.IntField() #opcional
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()

    #nombre
    #id_producto <- id_producto
    #unidad = dbMongo.IntField()
    #EmbeddedDocu#ment
    


class ProductoEnStockSchema(Schema):
    id_espacioFisico = fields.Integer()
    codigoContenedor = fields.Integer()
    detalleUbicacion = fields.String(default="")
    unidad = fields.Integer()
    codigoContenedor =  fields.Integer(null=True)
    unidad = fields.Integer(default=1)

class ProductoNuevoStockSchema(ProductoEnStockSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_espaciofisico", "code": 400}})
  


    