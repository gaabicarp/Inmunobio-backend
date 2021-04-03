from db import dbMongo
import datetime
from marshmallow import Schema, fields
from dateutil import parser
from flask import jsonify
class Proyecto(dbMongo.Document):
    nombre = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFinal = dbMongo.DateTimeField(required=False)
    finalizado = dbMongo.BoolField(default=False)
    montoInicial = dbMongo.FloatField()
    conclusion = dbMongo.StringField(required=False)

    def guardar(self):
        self.save()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(finalizado=False).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(_id=str(id)).first()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return cls.query.filter_by(nombre=_nombre).all()

    def json(self):
        proyectoSchema = ProyectoSchema()
        return jsonify(proyectoSchema.dump(self))
class ProyectoSchema(Schema):
    _id = fields.Str(dump_only=True)
    nombre = fields.Str()
    descripcion = fields.Str()
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float()
    conclusion = fields.Str()