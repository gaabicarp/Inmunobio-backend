
from marshmallow import Schema, fields, post_load
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
    id_fuenteExperimental = fields.Int()

    @post_load
    def make_muestraExterna(self, data, **kwargs):
        return MuestraExterna(**data)


class MuestraExternaSchema(MuestraExternaSchema):
    id_muestra = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la muestra externa", "code": 400}})
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})