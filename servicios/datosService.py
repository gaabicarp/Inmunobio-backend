from schemas.datosSchema import DatosSchema

class DatosService:

    @classmethod
    def llenarBase(cls,datos):
        datosObject = DatosSchema().load(datos)
        print(datosObject)
        [ unObj.save() for unObj in datosObject['proyecto'] ]
   
    @classmethod
    def llenarBaseMysql(cls,datos):
        datosObject = ().load(datos)
        [ unObj.save() for unObj in datosObject['proyecto'] ]