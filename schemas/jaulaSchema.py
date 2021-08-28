
from marshmallow import Schema, fields, post_load
from models.mongo.jaula import Jaula
from schemas.blogSchema import BlogSchema

class JaulaSchema(Schema):
    id_jaula = fields.Int()
    id_proyecto = fields.Int()
    id_espacioFisico = fields.Int()
    codigo = fields.Str()
    rack = fields.Int()
    estante = fields.Int()
    tipo = fields.Str()
    capacidad = fields.Int()
    habilitado = fields.Bool()
#    blogs = fields.Nested(BlogSchema, many=True)

class JaulaSchemaBlogs(JaulaSchema):
    blogs = fields.Nested(BlogSchema, many=True)

class NuevaJaulaSchema(Schema):
    id_espacioFisico = fields.Int(required=True, error_messages={"required" : {"message" : "Es necesario indicar el id del espacio físico", "code": 400}})
    codigo = fields.Str(required=True, error_messages={"required": {"message" : "Es necesario indicar el código de la jaula", "code": 400}})
    rack = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el número de rack donde va a estar ubicada la jaula", "code": 400}})
    estante = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el número del estante", "code": 400}})
    capacidad = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar la capacidad de la jaula", "code": 400}})
    id_proyecto = fields.Int()
    tipo = fields.Str()

    @post_load
    def makeJaula(self, data, **kwargs):
        return Jaula(**data)

class ActualizarProyectoJaulaSchema(JaulaSchema):
    id_jaula = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula", "code" : 400}})
    id_proyecto = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    
    @post_load
    def makeJaula(self, data, **kwargs):
        return Jaula(**data)

class ActualizarJaulaSchema(JaulaSchema):
    id_jaula = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula", "code" : 400}})

class NuevoBlogJaulaSchema(Schema):
    id_jaula = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula", "code" : 400}})
    blogs = fields.Nested(BlogSchema,required=True, error_messages={"required": {"message" : "Es necesario indicar datos de blog de jaula", "code" : 400}})

class BusquedaBlogsJaula(Schema):
    fechaDesde = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-desde.", "code": 400}}) 
    fechaHasta = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-hasta", "code": 400}}) 

class BusquedaBlogJaula(BusquedaBlogsJaula):
    id_jaula = fields.Integer(required=True,error_messages={"required": {"message": "Debe indicarse  id_jaula", "code": 400}}) 

class JaulaBaseSchema(NuevaJaulaSchema):
    blogs = fields.Nested(BlogSchema,required=True, error_messages={"required": {"message" : "Es necesario indicar datos de blog de jaula", "code" : 400}},many=True)

