from db import dbMongo
import datetime
from marshmallow import Schema, fields, post_load, ValidationError
from bson import ObjectId
from dateutil import parser
from models.mysql.usuario import Usuario
 
class Proyecto(dbMongo.Document):

    id_proyecto = dbMongo.SequenceField()
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

    def json(self):
        proyectoSchema = ProyectoSchema()
        return proyectoSchema.dump(self)

class ProyectoSchema(Schema):
    id_proyecto = fields.Integer()
    codigoProyecto = fields.Str()
    nombre = fields.Str()
    descripcion = fields.Str()
    participantes = fields.List(fields.Int())
    idDirectorProyecto = fields.Int()
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float()
    conclusion = fields.Str()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Proyecto(**data)
    
class ProyectoNuevoSchema(ProyectoSchema):
    codigoProyecto = fields.Str(required=True, error_messages={"required": {"message": "Se necesita el código del proyecto", "code": 400}})
    nombre = fields.Str(required=True, error_messages={"required": {"message": "Se necesita ingresar el nombre del proyecto", "code": 400}})
    montoInicial = fields.Float(required=True, error_messages={"required": {"message": "Se necesita ingresar un monto inicial", "code": 400}})

class ProyectoCerradoSchema(ProyectoSchema):
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto", "code:": 400}})
    conclusion = fields.Str(required=True, error_messages={"required": {"message": "Es necesario detallar la conclusión para cerrar el proyecto", "code": 400}})
    
class ProyectoModificarSchema(ProyectoSchema):

    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto. Este campo no puede estar vacío", "code:": 400}})
    descripcion = fields.Str(required=True, error_messages={"required": {"message": "Es necesaria una descripcion. Este campo puede estar vacío", "code": 400}})
    montoInicial = fields.Float(required=True, error_messages={"required": {"message": "Es necesario un montoInicial. Este campo no puede estar vacío.", "code": 400}})