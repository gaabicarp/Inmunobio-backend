from db import dbMongo
import datetime
from dateutil import parser
from marshmallow import Schema, fields, post_load

class MuestraExterna(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.SequenceField()
    codigo = dbMongo.StringField()
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
class Experimento(dbMongo.Document):
    id_experimento = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFin = dbMongo.DateTimeField()
    resultados = dbMongo.StringField(default="")
    finalizado = dbMongo.BooleanField(default=False)
    metodologia = dbMongo.StringField()
    conclusiones = dbMongo.StringField(default="")
    objetivos = dbMongo.StringField()
    muestrasExternas = dbMongo.ListField(dbMongo.EmbeddedDocumentField(MuestraExterna))

    def json(self):
        return ExperimentoSchema().dump(self)

class MuestraExternaSchema(Schema):
    id_muestra = fields.Int()
    codigo = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
class ExperimentoSchema(Schema):
    id_experimento = fields.Int()
    id_proyecto = fields.Int()
    fechaInicio = fields.DateTime()
    fechaFin = fields.DateTime()
    resultados = fields.Str()
    finalizado = fields.Boolean()
    metodologia = fields.Str()
    conclusiones = fields.Str()
    objetivos = fields.Str()
    muestrasExternas = fields.Nested(MuestraExternaSchema, many=True)

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Experimento(**data)
class AltaExperimentoSchema(ExperimentoSchema):

    id_proyecto = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    metodologia = fields.Str( required=True, error_messages={"required": {"message": "El campo metodología es necesario, no puede estar vacío", "code": 400}})
    objetivos = fields.Str(required=True, error_messages={"required": {"message": "El campo objetivos es necesario, no puede estar vacío", "code": 400}})
class CerrarExperimentoSchema(ExperimentoSchema):

    id_experimento = fields.Int(required=True, error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}})
    resultados = fields.Str(required=True, error_messages={"required": {"message": "El campo resultados es necesario, no puede estar vacío", "code": 400}})
    conclusiones = fields.Str(required=True, error_messages={"required": {"message": "El campo resultados es necesario, no puede estar vacío", "code": 400}})
class ModificarExperimentoSchema(ExperimentoSchema):
    id_experimento = fields.Int(required=True, error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}})

