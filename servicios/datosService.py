from models.mongo.contenedor import Contenedor
from schemas.datosSchema import DatosSchema
from exceptions.exception import ErrorContenedorInexistente

class DatosService:

    @classmethod
    def llenarBase(cls,datos):
        datosObject = DatosSchema().load(datos)
        print(datosObject)
        [ unObj.save() for unObj in datosObject['proyecto'] ]

