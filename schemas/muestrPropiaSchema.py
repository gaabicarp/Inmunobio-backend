from marshmallow import Schema, fields, post_load
from models.mongo.muestraPropia import MuestraPropia

class MuestraPropiaSchema(Schema):
    id_muestra = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    nombre = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
    id_fuenteExperimental = fields.Int()

    @post_load
    def makeMuestraPropia(self, data, **kwargs):
        return MuestraPropia(**data)