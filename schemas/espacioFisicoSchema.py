from marshmallow import Schema, fields, post_load
from models.mongo.espacioFisico import EspacioFisico
from schemas.blogSchema import NuevoBlogSchema,BlogSchema

class EspacioFisicoSchema(Schema):
    nombre = fields.String()
    piso = fields.String()
    sala = fields.String()
    descripcion = fields.String()
    blogs = fields.Nested(BlogSchema,many=True)
    id_espacioFisico = fields.Integer()
    #tipo = dbMongo.StringField() #Revisar y preguntar /Taller, Bioterio, etc

class ModificarEspacioFisico(EspacioFisicoSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Deben indicarse el id del espacio", "code": 400}})
    blogs = fields.Nested(BlogSchema,many=True,dump_only=True)

class NuevoEspacioFisicoSchema(Schema):
    nombre = fields.String(required=True, error_messages={"required": {"message" : "Deben indicarse el nombre del espacio", "code": 400}})
    piso = fields.String()
    sala = fields.String()
    descripcion = fields.String()

    @post_load
    def makeEspacio(self, data, **kwargs):
        return EspacioFisico(**data)

class NuevoBlogEspacioFisicoSchema(Schema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Deben indicarse el id del espacio", "code": 400}})
    blogs = fields.Nested(NuevoBlogSchema)

    
 