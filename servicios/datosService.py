from schemas.datosSchema import DatosSchema,DatosMysql

from marshmallow import EXCLUDE

class DatosService:

    @classmethod
    def llenarBase(cls,datos):
        datosObject = DatosSchema().load(datos)
        [ [ unObj.save() for unObj in value]for key,value in datosObject.items() ]
        
    @classmethod
    def llenarBaseMysql(cls,datos):
        DatosMysql().load(datos,unknown=EXCLUDE)


   