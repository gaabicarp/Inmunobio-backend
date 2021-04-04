from db import dbMongo
import datetime
from marshmallow import Schema, fields
from bson import ObjectId
from dateutil import parser
from flask import jsonify
class Proyecto(dbMongo.Document):
    idProyecto = dbMongo.SequenceField()
    codigoProyecto = dbMongo.StringField()
    nombre = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFinal = dbMongo.DateTimeField()
    finalizado = dbMongo.BooleanField(default=False)
    montoInicial = dbMongo.DecimalField()
    conclusion = dbMongo.StringField()

    def guardar(self):
        self.save()

    @classmethod
    def find_all(cls):
        return cls.objects.filter(finalizado=False).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.objects.filter(idProyecto=id).first()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return cls.objects(nombre = _nombre).first()

    def json(self):
        proyectoSchema = ProyectoSchema()
        return proyectoSchema.dump(self)

Schema.TYPE_MAPPING[ObjectId] = fields.String
class ProyectoSchema(Schema):
    idProyecto = fields.Str()
    codigoProyecto = fields.Str()
    nombre = fields.Str()
    descripcion = fields.Str()
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float()
    conclusion = fields.Str()

    class Meta:
        model : Proyecto
        #datetimeformat = '%Y-%m-%dT%H:%M:%SZ'