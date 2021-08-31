from marshmallow import Schema, fields, post_load
from mongoengine.errors import ValidationError
from models.mongo.grupoExperimental import GrupoExperimental
from schemas.fuenteExperimentalPropia import FuenteExperimentalPropiaSchema,FuenteExperimentalPropiaOtroSchema
from schemas.muestrPropiaSchema import MuestraPropiaSchema
from models.mongo.validacion import Validacion

class GrupoExperimentalSchema(Schema):
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str(default="")
    tipo = fields.Str()
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaSchema,  many=True)
    muestras = fields.Nested(MuestraPropiaSchema, many=True) #Guardar muestra propias (copia)
    parent = fields.Int()
    habilitado = fields.Bool()

    @post_load
    def makeGrupo(self, data, **kwargs):
        return GrupoExperimental(**data)

def tipoGrupo(data):
    if (not Validacion.not_empty_string(data)) or (data != "Animal" and data !=  "Otro"): raise ValidationError('El tipo debe ser Animal u Otro'  )

class AltaGrupoExperimentalSchema(GrupoExperimentalSchema):
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del experimento", "code": 400}})
    codigo = fields.Str( required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "Es necesario indicar el codigo del grupo experimental", "code": 400}})
    tipo = fields.Str(required=True, validate=tipoGrupo , error_messages={"required": {"message": "Es necesario indicar el tipo del grupo experimental", "code": 400}})
    descripcion = fields.Str(required=True, validate=Validacion.not_empty_string , error_messages={"required": {"message": "Es necesario indicar una breve descripción al grupo experimental", "code": 400}})

class AgregarFuentesAlGrupoExperimentalSchema(GrupoExperimentalSchema):
    id_grupoExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del grupo experimental", "code": 400}})
    #codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required" : {"message": "Es necesario indicar el codigo del grupo experimental", "code": 400}})
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required" : {"message" : "Se deben enviar fuentes experimentales.", "code": 400}})

class DividirGrupoExperimentalSchema(AltaGrupoExperimentalSchema):
    parent = fields.Int(required=True,validate=Validacion.not_empty_int, error_messages={'required': {"message" : "Se debe indicar el id del grupo experimental del cuál proviene este nuevo grupo.", "code": 400}})

class DividirGrupoExperimentalOtroSchema(AltaGrupoExperimentalSchema):
    #fuentesExperimentales = fields.Nested(FuenteExperimentalOtroSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required" : {"message" : "Se deben enviar fuentes experimentales.", "code": 400}})
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaOtroSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required" : {"message" : "Se deben enviar fuentes experimentales.", "code": 400}})
    parent = fields.Int(required=True,validate=Validacion.not_empty_int, error_messages={'required': {"message" : "Se debe indicar el id del grupo experimental del cuál proviene este nuevo grupo.", "code": 400}})

class GrupoDeTipoOtro(GrupoExperimentalSchema):
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaOtroSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required" : {"message" : "Se deben enviar fuentes experimentales.", "code": 400}})
