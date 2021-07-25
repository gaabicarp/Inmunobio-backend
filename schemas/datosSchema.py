from marshmallow import Schema, fields
from .usuarioSchema import UsuarioSchema
from .proyectoSchema import ProyectoSchema

class DatosSchema(Schema):
    proyecto = fields.Nested(ProyectoSchema,many=True)

class DatosSchemaMysql(Schema):
    usuarios = fields.Nested(UsuarioSchema,many=True)
    permisos = fields.Nested(UsuarioSchema,many=True)

    