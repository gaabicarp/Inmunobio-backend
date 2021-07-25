from db import dbMongo
import datetime
from dateutil import parser
from marshmallow import Schema, fields, post_load, validate

from models.mongo.validacion import Validacion

class Muestra(dbMongo.Document):
    id_muestra = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    id_grupoExperimental = dbMongo.IntField()
    id_experimento = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
    id_contenedor= dbMongo.IntField()
    habilitada = dbMongo.BooleanField(default=True)

    def json(self):
        return MuestraSchema().dump(self)
class MuestraSchema(Schema):
    id_muestra = fields.Int()
    id_proyecto = fields.Int()
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
    id_contenedor = fields.Int()
    habilitada = fields.Boolean()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Muestra(**data)

class NuevaMuestraSchema(MuestraSchema):
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    id_grupoExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del grupo experimental", "code":400}})
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del experimento", "code":400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el id código de la muestra", "code": 400}})
    descripcion = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar una descripcion", "code": 400}})
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del contenedor", "code": 400}})

class ModificarMuestraSchema(MuestraSchema):
    id_muestra = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del muestra", "code":400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el id código de la muestra", "code": 400}})
    descripcion = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar una descripcion", "code": 400}})
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del contenedor", "code": 400}})

