from db import dbMongo
import datetime
from marshmallow import Schema, fields
class Proyecto(dbMongo.Document):
    nombre = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    fechaInicio = dbMongo.DateTimeField(default=datetime.datetime.now)
    fechaFinal = dbMongo.DateTimeField()
    finalizado = dbMongo.BoolField(default=False)
    montoInicial = dbMongo.FloatField()
    conclusion = dbMongo.StringField()

    def __init__(self, nombre, descripcion, montoInicial):
        self.nombre = nombre
        self.descripcion = descripcion
        self.montoInicial = montoInicial

    @classmethod
    def guardar(cls):
        cls.save()

    @classmethod
    def find_all(cls):
        return cls.query.filter_by(finalizado=False).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(_id=str(id)).first()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return cls.query.filter_by(nombre=_nombre).all()
class ProyectoSchema(Schema):
    _id = fields.Str(dump_only=True)
    nombre = fields.Str()
    descripcion = fields.Str()
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Decimal()
    conclusion = fields.Str()