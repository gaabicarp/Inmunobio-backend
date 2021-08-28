from marshmallow import Schema, fields, post_load
from models.mysql.permiso import Permiso

class PermisoSchema(Schema):
    descripcion = fields.Str()
    @post_load
    def makePermiso(self, data, **kwargs):
        return Permiso(**data)

class PermisoBase(PermisoSchema):
    @post_load
    def makePermiso(self, data, **kwargs):
        from db import db
        db.session.add(Permiso(**data))
        db.session.commit()

class PermisoExistenteSchema(Schema):
    id_permiso = fields.Integer( required=True,error_messages={"required": {"message": "Debe indicarse el id del permiso", "code": 400}})
    descripcion = fields.Str( required=True,error_messages={"required": {"message": "Debe indicarse la descripcion del permiso", "code": 400}})
