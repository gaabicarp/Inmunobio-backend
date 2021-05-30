from marshmallow import Schema, fields, post_load
from models.mongo.espacioFisico import EspacioFisico
from schemas.blogSchema import BlogSchema

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

class NuevoEspacioFisicoSchema(EspacioFisicoSchema):
    id_espacioFisico = fields.Integer(dump_only=True)
    nombre = fields.String(required=True, error_messages={"required": {"message" : "Deben indicarse el nombre del espacio", "code": 400}})
    blogs = fields.Nested(BlogSchema,many=True, dump_only=True)
    
    @post_load
    def makeEspacio(self, data, **kwargs):
        return EspacioFisico(**data)
 