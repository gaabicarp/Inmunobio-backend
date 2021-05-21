from marshmallow import Schema, fields, post_load

class PermisoSchema(Schema):
    id_permiso = fields.Integer()
    descripcion = fields.Str()
   
class PermisoExistenteSchema(PermisoSchema):
    id_permiso = fields.Integer( required=True,error_messages={"required": {"message": "Debe indicarse el id del permiso", "code": 400}})
    descripcion = fields.Str( required=True,error_messages={"required": {"message": "Debe indicarse la descripcion del permiso", "code": 400}})
