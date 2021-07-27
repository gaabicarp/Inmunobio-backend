from schemas.datosSchema import DatosSchema,DatosUsuarioMysql,DatosPermisoMysql
from marshmallow import EXCLUDE

class DatosService:

    @classmethod
    def llenarBase(cls,datos):
        datosObject = DatosSchema().load(datos)
        [ unObj.save() for unObj in datosObject['proyecto'] ]

    @classmethod
    def llenarBaseMysql(cls,datos):
        datosPermisos = DatosPermisoMysql().load(datos,unknown=EXCLUDE )
        [ cls.commitDatos(unObj) for unObj in datosPermisos['permiso']]
        datosUser = DatosUsuarioMysql().load(datos,unknown=EXCLUDE)
        [ cls.commitDatos(unObj) for unObj in datosUser['usuario']]

    @classmethod
    def commitDatos(cls,datos):
        from db import db
        db.session.add(datos)
        db.session.commit()