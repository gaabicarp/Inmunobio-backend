from db import dbMongo
from marshmallow import Schema, fields, post_load
from models.mongo.herramienta import Herramienta
from schemas.blogSchema import NuevoBlogSchema
from models.mongo.validacion import Validacion

class HerramientaSchema(Schema):
    nombre = fields.String()
    detalle = fields.String()
    id_herramienta = fields.Integer()
    id_espacioFisico = fields.Integer()

class NuevaHerramientaSchema(Schema):
    nombre = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse el nombre de la herramienta", "code": 400}})
    detalle = fields.String()
    id_espacioFisico = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse espacio fisico", "code": 400}}) 

    @post_load
    def makeHerramienta(self, data, **kwargs):
        return Herramienta(**data)

class HerramientaBaseSchema(NuevaHerramientaSchema):
    blogs = fields.Nested(NuevoBlogSchema,required=True, error_messages={"required": {"message" : "Es necesario indicar datos de blog ", "code" : 400}},many=True)
  
class NuevoBlogHerramientaSchema(Schema):
    blogs = fields.Nested(NuevoBlogSchema,required=True, validate=Validacion.not_empty_list,error_messages={"required": {"message" : "Es necesario indicar datos de blog ", "code" : 400}})
    id_herramienta = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse  id_herramienta", "code": 400}}) 

class BusquedaBlogHerramienta(Schema):
    fechaDesde = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse  fecha-desde.", "code": 400}}) 
    fechaHasta = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse  fecha-hasta", "code": 400}}) 
    id_herramienta = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse  id_herramienta", "code": 400}}) 

