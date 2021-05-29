from models.mysql.usuario import Usuario
from marshmallow import Schema, fields, post_load,ValidationError
from schemas.permisosSchema import PermisoSchema,PermisoExistenteSchema

class UsuarioSchema(Schema):
    id_usuario = fields.Integer(dump_only=True)
    email = fields.Str()
    nombre = fields.Str()
    password = fields.Str()    
    habilitado = fields.Boolean(default=True)
    direccion = fields.Str()
    telefono = fields.Str()
    permisos = fields.Nested(PermisoSchema, many=True)
    id_grupoDeTrabajo =fields.Integer()
    esJefeDe = fields.Integer()

def must_not_be_blank(data):
    if not data:
        raise ValidationError('Deben asignarse permisos .')

class UsuarioNuevoSchema(UsuarioSchema):
    email = fields.Str( required=True,error_messages={"required": {"message": "Se necesita ingresar el mail", "code": 400}})
    nombre = fields.Str( required=True,error_messages={"required": {"message": "Se necesita ingresar el nombre del usuario", "code": 400}})
    password = fields.Str(required=True,error_messages={"required": {"message": "Se necesita ingresar el password", "code": 400}})
    permisos = fields.Nested(PermisoExistenteSchema, many=True, required=True,error_messages={"required": {"message": "Se necesita asignar permisos", "code": 400}},validate=must_not_be_blank)
    
    @post_load
    def make_Usuario(self, data, **kwargs):
        return Usuario(**data)

class usuarioIDSchema(Schema):
    id_usuario = fields.Integer(required=True,error_messages={"required": {"message": "Debe indicarse id Usuario", "code": 400}})

class UsuarioSchemaModificar(usuarioIDSchema):

    email = fields.Str()
    password = fields.Str()    
    direccion = fields.Str()
    telefono = fields.Str()
    nombre = fields.Str()
    permisos = fields.Nested(PermisoExistenteSchema, many=True)
    habilitado = fields.Boolean(default=True)
    direccion = fields.Str()
    id_grupoDeTrabajo =fields.Integer()
    esJefeDe = fields.Integer()
    

