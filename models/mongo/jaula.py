from db import dbMongo
from models.mongo.blog import Blog, BlogSchema
from marshmallow import Schema, fields, post_load

class Jaula(dbMongo.Document):
    id_jaula = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField(default=0)
    nombre_proyecto = dbMongo.StringField(default="")
    id_espacio_fisico = dbMongo.IntField()
    codigo = dbMongo.StringField()
    rack = dbMongo.IntField()
    estante = dbMongo.IntField()
    tipo = dbMongo.StringField()
    capacidad = dbMongo.IntField()
    habilitado = dbMongo.BooleanField(default = True)
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentListField('Blog'))

    def json(self):
        return JaulaSchema().dump(self)

class JaulaSchema(Schema):
    id_jaula = fields.Int()
    id_proyecto = fields.Int()
    nombre_proyecto = fields.Str()
    id_espacio_fisico = fields.Int()
    codigo = fields.Str()
    rack = fields.Int()
    estante = fields.Int()
    tipo = fields.Str()
    capacidad = fields.Int()
    habilitado = fields.Bool()
    blogs = fields.Nested('BlogSchema', many=True)

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Jaula(**data)

class NuevaJaulaSchema(JaulaSchema):
    id_espacio_fisico = fields.Int(required=True, error_messages={"required" : {"message" : "Es necesario indicar el id del espacio físico", "code": 400}})
    codigo = fields.Str(required=True, error_messages={"required": {"message" : "Es necesario indicar el código de la jaula", "code": 400}})
    rack = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el número de rack donde va a estar ubicada la jaula", "code": 400}})
    estante = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el número del estante", "code": 400}})
    capacidad = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar la capacidad de la jaula", "code": 400}})

class ActualizarProyectoJaulaSchema(JaulaSchema):
    id_jaula = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula", "code" : 400}})
    id_proyecto = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    nombre_proyecto = fields.String(required=True, error_messages={"required": {"message" : "Es necesario indicar el nombre de proyecto", "code" : 400}})

class ActualizarJaulaSchema(JaulaSchema):
    id_jaula = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula", "code" : 400}})