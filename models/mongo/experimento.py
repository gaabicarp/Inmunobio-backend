from db import dbMongo
from flask import jsonify
import datetime
from dateutil import parser
from marshmallow import Schema, fields, post_load
class Experimento(dbMongo.Document):
    id_experimento = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFin = dbMongo.DateTimeField()
    resultados = dbMongo.StringField()
    finalizado = dbMongo.BooleanField(default=False)
    metodologia = dbMongo.StringField()
    conclusiones = dbMongo.StringField()
    objetivos = dbMongo.StringField()
    gruposExperimentales = dbMongo.ListField(dbMongo.IntField())

    @classmethod
    def find_by_id(cls, idExperimento):
        return cls.objects.filter(id_experimento=idExperimento).first()

    @classmethod
    def find_all_by_idProyecto(cls, idProyecto):
        return ExperimentoSchema().dump(cls.objects.filter(id_proyecto=idProyecto).all(), many=True)
    
    @classmethod
    def cerrarExperimento(cls, idExperimento, datos):
        cls.objects(id_experimento = idExperimento).update(s)

    def json(self):
        return ExperimentoSchema().dump(self)


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
    gruposExperimentales = fields.List(fields.Int())

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Experimento(**data)
class AltaExperimentoSchema(Schema):

    id_experimento = fields.Int()
    id_proyecto = fields.Int()
    fechaInicio = fields.Int()
    fechaFin = fields.DateTime()
    resultados = fields.Str()
    finalizado = fields.Boolean()
    metodologia = fields.Str( required=True,
        error_messages={"required": {"message": "El campo metodología es necesario, no puede estar vacío", "code": 400}},
        )
    conclusiones = fields.Str()
    objetivos = fields.Str(required=True,
        error_messages={"required": {"message": "El campo objetivos es necesario, no puede estar vacío", "code": 400}},
        )
    gruposExperimentales = fields.List(fields.Int())

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Experimento(**data)

class CerrarExperimentoSchema(Schema):

    id_experimento = fields.Int(required=True,
        error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}},
        )
    id_proyecto = fields.Int()
    fechaInicio = fields.Int()
    
    resultados = fields.Str(required=True,
        error_messages={"required": {"message": "El campo resultados es necesario, no puede estar vacío", "code": 400}},
        )
    finalizado = fields.Boolean()
    metodologia = fields.Str()
    conclusiones = fields.Str(required=True,
        error_messages={"required": {"message": "El campo resultados es necesario, no puede estar vacío", "code": 400}},
        )
    objetivos = fields.Str()
    gruposExperimentales = fields.List(fields.Int())
