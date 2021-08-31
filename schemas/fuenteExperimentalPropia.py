from marshmallow import Schema, fields, post_load,post_dump
from models.mongo.fuenteExperimentalPropia import FuenteExperimentalPropia

class FuenteExperimentalPropiaSchema(Schema):
    id_fuenteExperimental = fields.Int()
    id_proyecto = fields.Int( allow_none=True)
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    especie = fields.Str( allow_none=True,default=None,missing=None)
    sexo = fields.Str( allow_none=True,default=None,missing=None)
    cepa = fields.Str( allow_none=True,default=None,missing=None)
    tipo = fields.Str( allow_none=True,default=None,missing=None)
    baja = fields.Bool(allow_none=True,default=None,missing=None)
    id_jaula = fields.Int(allow_none=True,default=None,missing=None)
    descripcion = fields.Str(default=None,missing=None)

    @post_load
    def makeFuentePropia(self, data, **kwargs):
        return FuenteExperimentalPropia(**data)

class FuenteExperimentalPropiaOtroSchema(Schema):
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    descripcion = fields.Str()
    id_fuenteExperimental = fields.Int()
    tipo = fields.Str()

    @post_load
    def makeFuentePropia(self, data, **kwargs):
        return FuenteExperimentalPropia(**data)



 
 
 