from marshmallow import Schema, fields, post_load
from models.mongo.espacioFisico import EspacioFisico
from schemas.blogSchema import NuevoBlogSchema,BlogSchema
from models.mongo.validacion import Validacion

class EspacioFisicoSchema(Schema):
    nombre = fields.String()
    piso = fields.String()
    sala = fields.String()
    descripcion = fields.String()
    id_espacioFisico = fields.Integer()
    #tipo = dbMongo.StringField() #Revisar y preguntar /Taller, Bioterio, etc

class ModificarEspacioFisico(EspacioFisicoSchema):
    id_espacioFisico = fields.Integer(required=True,validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Deben indicarse el id del espacio", "code": 400}})
    blogs = fields.Nested(BlogSchema,many=True)

class NuevoEspacioFisicoSchema(Schema):
    nombre = fields.String(required=True,validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Deben indicarse el nombre del espacio fisico", "code": 400}})
    piso = fields.String(required=True,validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Deben indicarse el piso del espacio fisico", "code": 400}})
    sala = fields.String(required=True,validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Deben indicarse la sala del espacio fisico", "code": 400}})
    descripcion = fields.String()

    @post_load
    def makeEspacio(self, data, **kwargs):
        return EspacioFisico(**data)

class EspacioFisicoBaseSchema(NuevoEspacioFisicoSchema):
    blogs = fields.Nested(BlogSchema,many=True)

class NuevoBlogEspacioFisicoSchema(Schema):
    id_espacioFisico = fields.Integer(required=True,validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Deben indicarse el id del espacio", "code": 400}})
    blogs = fields.Nested(NuevoBlogSchema,required=True,error_messages={"required": {"message" : "Deben indicarse datos del blog de espacio físico.", "code": 400}})

class BusquedaBlogEspacio(Schema):
    fechaDesde = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse  fecha-desde.", "code": 400}}) 
    fechaHasta = fields.String(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse  fecha-hasta", "code": 400}}) 
    id_espacioFisico = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse  id_espacioFisico", "code": 400}}) 

