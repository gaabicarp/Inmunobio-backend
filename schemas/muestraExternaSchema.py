
from marshmallow import Schema, fields, post_load, validate
from models.mongo.validacion import Validacion
from models.mongo.muestraExterna import MuestraExterna

class MuestraExternaSchema(Schema):
    id_muestra = fields.Int()
    codigo = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
    id_proyecto = fields.Int()
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    descripcion = fields.Str()
    id_contenedor = fields.Int()
    habilitada = fields.Boolean()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return MuestraExterna(**data)