from marshmallow import Schema, fields, post_load
from models.mongo.fuenteExperimentalPropia import FuenteExperimentalPropia

class FuenteExperimentalPropiaSchema(Schema):
    id_fuenteExperimental = fields.Int()
    id_proyecto = fields.Int()
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    especie = fields.Str()
    #sexo = fields.Str(required=False, allow_none=True)
    sexo = fields.Str()
    cepa = fields.Str()
    tipo = fields.Str()
    #baja = fields.Bool(required=False, allow_none=True)
    #id_jaula = fields.Int(required=False, allow_none=True)
    #descripcion = fields.Str(required=False, allow_none=True)
    baja = fields.Bool(allow_none=True)
    id_jaula = fields.Int(allow_none=True)
    descripcion = fields.Str(allow_none=True)
    @post_load
    def makeFuentePropia(self, data, **kwargs):
        return FuenteExperimentalPropia(**data)