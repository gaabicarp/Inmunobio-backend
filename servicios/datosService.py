from schemas.datosSchema import DatosSchema,DatosMysql

from marshmallow import EXCLUDE

class DatosService:

    @classmethod
    def llenarBase(cls,datos):
        datosObject = DatosSchema().load(datos)
        [ unObj.save() for unObj in datosObject['proyecto'] ]

    @classmethod
    def llenarBaseMysql(cls,datos):
        DatosMysql().load(datos,unknown=EXCLUDE)


   