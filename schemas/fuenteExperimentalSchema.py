from marshmallow import fields
from schemas.animalSchema import AnimalSchema
from models.mongo.validacion import Validacion

class FuenteExperimentalSchema(AnimalSchema):
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    descripcion = fields.Str()

class FuenteExperimentalAnimalSchema(FuenteExperimentalSchema):
    id_fuenteExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la fuente experimental", "code": 400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el codigo de la fuente experimental", "code": 400}})
    codigoGrupoExperimental = fields.Str(required=True, validate=Validacion.not_empty_string,  error_messages={"required" : "Es necesario indicar el código para el grupo experimental", "code" : 400})
    
class FuenteExperimentalAnimalBSchema(FuenteExperimentalSchema):
    id_fuenteExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la fuente experimental", "code": 400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el codigo de la fuente experimental", "code": 400}})

class FuenteExperimentalOtroSchema(FuenteExperimentalSchema):
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string,  error_messages={"required": {"message" : "Es necesario indicar el codigo de la fuente experimental", "code": 400}})
    #codigoGrupoExperimental = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required" : "Es necesario indicar el código para el grupo experimental", "code" : 400})
    tipo = fields.Str(required=True, validate=Validacion.not_empty_string,  error_messages={"required" : {"message" : "Es necesario indicar el tipo de la fuente experimental", "code": 400}})
    descripcion = fields.Str(required=True, validate=Validacion.not_empty_string,  error_messages={"required" : {"message" : "Es necesario indicar una descripcion cuando la fuente no es de tipo animal", "code": 400}})
    id_fuenteExperimental = fields.Int(missing=None)
    id_proyecto = fields.Int(missing=None)
    especie = fields.Str(missing=None)
    sexo = fields.Str(missing=None)
    cepa = fields.Str(missing=None)
    id_jaula = fields.Int(missing=None)
    baja = fields.Boolean(missing=None)