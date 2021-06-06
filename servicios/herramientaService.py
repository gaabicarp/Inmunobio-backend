from models.mongo.herramienta import Herramienta
from servicios.fuenteExperimentalService import FuenteExperimentalService
from servicios.blogService import BlogService
from exceptions.exception import ErrorHerramientaInexistente
from schemas.herramientaSchema import NuevaHerramientaSchema,HerramientaSchema

class HerramientaService:
    @classmethod
    def find_by_id(cls, _id_herramienta):
        herramienta =  Herramienta.objects(id_herramienta = _id_herramienta).first()
        if not herramienta : raise ErrorHerramientaInexistente(_id_herramienta)
        return herramienta

    @classmethod
    def nuevaHerramienta(cls,datos):
        herramienta = NuevaHerramientaSchema().load(datos)
        herramienta.save()

    @classmethod
    def modificarHerramienta(cls,datos):
        HerramientaSchema.load(datos)
        herramienta =  cls.find_by_id(datos['id_herramienta'])
        herramienta.update(
            nombre = datos['nombre'],
            detalle = datos['detalle'],
            id_espacioFisico =datos['id_espacioFisico']
        )
        herramienta.save()

    @classmethod
    def eliminarHerramienta(cls,id_herramienta):
        herramienta =  cls.find_by_id(id_herramienta)
        herramienta.delete()
    @classmethod
    def obtenerHerramientas(cls):
        return Herramienta.objects.all()

        








    