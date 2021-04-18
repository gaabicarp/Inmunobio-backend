from db import dbMongo
import datetime
from marshmallow import Schema, fields, post_load, ValidationError
class Contenedor(Document):
    id_contenedor = dbMongo.SequenceField()
    codigo = dbMongo.StringField()
    nombre = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    temperatura = dbMongo.StringField()
    id_proyecto = IntegerField()
    #La capacidad la manejan ellos.
    capacidad = IntegerField()
    fichaTecnica = dbMongo.StringField()
    disponible = booleanField(default=true)
    parent = dbMongo.Integer(default = 0)
class ContenedorSchema(Schema):
    id_contenedor = fields.Integer()
    codigo = fields.Str()
    nombre = fields.Str()
    descripcion = fields.Str()
    temperatura = fields.Str()
    fichaTecnica = fields.Str()
    disponible = fields.Boolean()
    parent = fields.Integer()
    
    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Contenedor(**data)