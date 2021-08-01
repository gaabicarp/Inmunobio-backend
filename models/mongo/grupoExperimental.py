from db import dbMongo
from marshmallow import Schema, fields, post_load, validate
import datetime
from dateutil import parser
from .fuenteExperimental import FuenteExperimentalSchema
from .validacion import Validacion

class MuestraPropia(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    nombre = dbMongo.StringField()
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()

class FuenteExperimentalPropia(dbMongo.EmbeddedDocument):
    id_fuenteExperimental = dbMongo.IntField()
    id_proyecto = dbMongo.IntField()
    codigo = dbMongo.StringField()
    codigoGrupoExperimental = dbMongo.StringField()
    especie = dbMongo.StringField()
    sexo = dbMongo.StringField(required=False, allow_none=True)
    cepa = dbMongo.StringField()
    tipo = dbMongo.StringField()
    baja = dbMongo.BooleanField(required=False, allow_none=True)
    id_jaula = dbMongo.IntField(required=False, allow_none=True)
    descripcion = dbMongo.StringField(required=False, allow_none=True)

class GrupoExperimental(dbMongo.Document):
    id_grupoExperimental = dbMongo.SequenceField()
    id_experimento = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    tipo = dbMongo.StringField()
    fuentesExperimentales = dbMongo.ListField(dbMongo.EmbeddedDocumentField(FuenteExperimentalPropia))
    muestras = dbMongo.ListField(dbMongo.EmbeddedDocumentField(MuestraPropia)) #Guardar muestra propias (copia)
    parent = dbMongo.IntField(default = 0)
    habilitado = dbMongo.BooleanField(default = True)

    def json(self):
        return GrupoExperimentalSchema().dump(self)

class MuestraPropiaSchema(Schema):
    id_muestra = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    nombre = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return MuestraPropia(**data)

class FuenteExperimentalPropiaSchema(Schema):
    id_fuenteExperimental = fields.Int()
    id_proyecto = fields.Int()
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    especie = fields.Str()
    sexo = fields.Str(required=False, allow_none=True)
    cepa = fields.Str()
    tipo = fields.Str()
    baja = fields.Bool(required=False, allow_none=True)
    id_jaula = fields.Int(required=False, allow_none=True)
    descripcion = fields.Str(required=False, allow_none=True)

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return FuenteExperimentalPropia(**data)
class GrupoExperimentalSchema(Schema):
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    tipo = fields.Str()
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaSchema,  many=True)
    muestras = fields.Nested(MuestraPropiaSchema, many=True) #Guardar muestra propias (copia)
    parent = fields.Int()
    habilitado = fields.Bool()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return GrupoExperimental(**data)
class AltaGrupoExperimentalSchema(GrupoExperimentalSchema):
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del experimento", "code": 400}})
    codigo = fields.Str( required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "Es necesario indicar el codigo del grupo experimental", "code": 400}})
    tipo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "Es necesario indicar el tipo del grupo experimental", "code": 400}})
class AgregarFuentesAlGrupoExperimentalSchema(GrupoExperimentalSchema):
    id_grupoExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del grupo experimental", "code": 400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required" : {"message": "Es necesario indicar el codigo del grupo experimental", "code": 400}})
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required" : {"message" : "Se deben enviar fuentes experimentales.", "code": 400}})

class DividirGrupoExperimentalSchema(AltaGrupoExperimentalSchema):
    parent = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={'required': {"message" : "Se debe indicar el id del grupo experimental del cuál se devidide", "code": 400}})
