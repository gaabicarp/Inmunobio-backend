from marshmallow import Schema, fields
from .usuarioSchema import UsuariosBase
from .proyectoSchema import ProyectoSchema
from.permisosSchema import PermisoBase

class DatosSchema(Schema):
    proyecto = fields.Nested(ProyectoSchema,many=True)


class DatosMysql(Schema):
    class Meta:
        ordered = True
    #Necesario para que al deserializar respete el orden en el que va el json

    permiso = fields.Nested(PermisoBase,many=True) 
    usuario = fields.Nested(UsuariosBase,many=True)

