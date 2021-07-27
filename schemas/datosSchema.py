from marshmallow import Schema, fields
from .usuarioSchema import UsuarioNuevoSchema
from .proyectoSchema import ProyectoSchema
from.permisosSchema import PermisoSchema
class DatosSchema(Schema):
    proyecto = fields.Nested(ProyectoSchema,many=True)

class DatosUsuarioMysql(Schema):
    usuario = fields.Nested(UsuarioNuevoSchema,many=True)

class DatosPermisoMysql(Schema):
    permiso = fields.Nested(PermisoSchema,many=True)
    