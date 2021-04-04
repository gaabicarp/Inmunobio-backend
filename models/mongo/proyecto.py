from db import dbMongo
import datetime
from marshmallow import Schema, fields, post_load, ValidationError
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
    participantes = dbMongo.ListField(dbMongo.IntField())
    idDirectorProyecto = dbMongo.IntField()

    def guardar(self):
        self.save()
    
    def crearProyecto(self, datos):
        self.codigoProyecto = datos['codigoProyecto']
        self.nombre = datos['nombre']
        self.save()

    @classmethod
    def find_all(cls):
        #return jsonify(UsuarioSchema().dump(usuarios, many=True))
        return jsonify(ProyectoSchema().dump(cls.objects.filter(finalizado=False).all(), many=True))
        

    @classmethod
    def find_by_id(cls, id):
        return cls.objects.filter(idProyecto=id).first()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return cls.objects(nombre = _nombre).first()
    
    @classmethod
    def cerrarProyecto(cls, _idProyecto, conclusion):
        proyecto = cls.objects(idProyecto = _idProyecto).first()
        proyecto.conclusion = conclusion
        proyecto.fechaFinal = default=parser.parse(str(datetime.datetime.utcnow()))
        proyecto.finalizado = True

    def json(self):
        proyectoSchema = ProyectoSchema()
        return proyectoSchema.dump(self)

#Schema.TYPE_MAPPING[ObjectId] = fields.String
class ProyectoSchema(Schema):
    idProyecto = fields.Str()
    codigoProyecto = fields.Str(
        required=True,
        error_messages={"required": {"message": "Se necesita el código del proyecto", "code": 400}},
        )
    nombre = fields.Str(
        required=True,
        error_messages={"required": {"message": "Se necesita ingresar el nombre del proyecto", "code": 400}},
    )
    descripcion = fields.Str()
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float(
        required=True,
        error_messages={"required": {"message": "Se necesita ingresar un monto inicial", "code": 400}},
        )
    conclusion = fields.Str()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Proyecto(**data)