from marshmallow import Schema, fields, post_load
from models.mongo.fuenteExperimental import FuenteExperimental
from models.mongo.validacion import Validacion

class AnimalSchema(Schema):
    id_fuenteExperimental = fields.Int()
    id_proyecto = fields.Int()
    especie = fields.Str()
    sexo = fields.Str()
    cepa = fields.Str()
    tipo = fields.Str()
    id_jaula = fields.Int()
    baja = fields.Boolean()

    @post_load
    def makeAnimal(self, data, **kwargs):
        return FuenteExperimental(**data)
        
class ExtendAnimal(AnimalSchema):
    codigoGrupoExperimental= fields.Str()

class AsignarAnimalAJaula(AnimalSchema):
    id_jaula = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula.", "code": 400}})
    id_fuenteExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la fuente experimental", "code": 400}})

class NuevoAnimalSchema(AnimalSchema):
    id_jaula = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la jaula.", "code": 400}})
    especie = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar la especie del animal", "code" : 400}})
    sexo = fields.Str(required=True, validate=Validacion.not_empty_string,  error_messages={"required": {"message" : "Es necesario indicar el sexo del animal", "code" : 400}})
    cepa = fields.Str(required=True, validate=Validacion.not_empty_string,  error_messages={"required": {"message" : "Es necesario indicar la cepa del animal", "code" : 400}})

