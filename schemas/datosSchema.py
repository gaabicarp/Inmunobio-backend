from marshmallow import Schema, fields
from .usuarioSchema import UsuarioSchema
from .proyectoSchema import ProyectoSchema

class DatosSchema(Schema):
    #usuario = fields.Nested(UsuarioSchema,many=True)
    proyecto = fields.Nested(ProyectoSchema,many=True)

    