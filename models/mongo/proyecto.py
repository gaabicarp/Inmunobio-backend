from db import dbMongo
import datetime
from marshmallow import Schema, fields, post_load, ValidationError
from bson import ObjectId
from dateutil import parser
from flask import jsonify
from models.mysql.usuario import Usuario
 
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
        return jsonify(ProyectoSchema().dump(cls.objects.filter(finalizado=False).all(), many=True))
        

    @classmethod
    def find_by_id(cls, id):
        return cls.objects.filter(idProyecto=id).first()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return cls.objects(nombre = _nombre).first()
    
    @classmethod
    def cerrarProyecto(cls, datos):
        proyecto = cls.objects(idProyecto = datos['idProyecto']).update(
            set__conclusion = datos['conclusion'],
            set__finalizado = True,
            set__fechaFinal = parser.parse(str(datetime.datetime.utcnow()))
        )
    
    @classmethod
    def modificarProyecto(cls, datos):
        if datos['descripcion'].strip() != "":
            proyecto = cls.objects(idProyecto =datos['idProyecto']).update(set__descripcion = datos['descripcion'])
        proyecto = cls.objects(idProyecto =datos['idProyecto']).update(set__montoInicial = datos['montoInicial'])
        
    def json(self):
        proyectoSchema = ProyectoSchema()
        return proyectoSchema.dump(self)
    @classmethod
    def agregarMiembros(self):
        usuariosIdPermitidas = Usuario.find_usuarios_Habilitados()
        return usuariosIdPermitidas

class ProyectoSchema(Schema):
    idProyecto = fields.Integer()
    codigoProyecto = fields.Str(
        required=True,
        error_messages={"required": {"message": "Se necesita el código del proyecto", "code": 400}},
        )
    nombre = fields.Str(
        required=True,
        error_messages={"required": {"message": "Se necesita ingresar el nombre del proyecto", "code": 400}},
    )
    descripcion = fields.Str()
    participantes = fields.List(fields.Int())
    idDirectorProyecto = fields.Int()
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
    
class ProyectoCerradoSchema(Schema):
    idProyecto = fields.Integer(
        required=True,
        error_messages={"required": {"message": "Es necesario el idProyecto", "code:": 400}},
    )
    codigoProyecto = fields.Str()
    nombre = fields.Str()
    descripcion = fields.Str()
    fechaInicio = fields.DateTime()
    participantes = fields.List(fields.Int())
    idDirectorProyecto = fields.Int()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float()
    conclusion = fields.Str(
        required=True,
        error_messages={"required": {"message": "Es necesario detallar la conclusión para cerrar el proyecto", "code": 400}},
    )

class ProyectoModificarSchema(Schema):
    idProyecto = fields.Integer(
        required=True,
        error_messages={"required": {"message": "Es necesario el idProyecto. Este campo no puede estar vacío", "code:": 400}},
    )
    codigoProyecto = fields.Str()
    nombre = fields.Str()
    participantes = fields.List(fields.Int())
    idDirectorProyecto = fields.Int()
    descripcion = fields.Str(
        required=True,
        error_messages={"required": {"message": "Es necesaria una descripcion. Este campo puede estar vacío", "code": 400}},
    )
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float(
        required=True,
        error_messages={"required": {"message": "Es necesario un montoInicial. Este campo no puede estar vacío.", "code": 400}},
    )
    conclusion = fields.Str()