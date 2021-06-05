from db import dbMongo
import datetime
from dateutil import parser
from marshmallow import Schema, fields, post_load

class Muestra(dbMongo.Document):
    id_muestra = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntegerField()
    codigo = dbMongo.StringField()
    fecha = dbMongo.dateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
    id_contenedor= dbMongo.IntegerField()

    def json(self):
        return MuestraSchema().dump(self)

class MuestraSchema(Schema):
    id_muestras = fields.Int()
    id_proyecto = fields.Int()
    codigo = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
    id_contenedor = fields.Int()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Muestra(**data)

class NuevaMuestraSchema(MuestraSchema):
    id_proyecto = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    codigo = fields.Str(required=True, error_messages={"required": {"message" : "Es necesario indicar el id código de la muestra", "code": 400}})
    id_contenedor = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id del contenedor", "code": 400}})


