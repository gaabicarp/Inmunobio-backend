from models.mongo.fuenteExperimental import FuenteExperimental
from schemas.fuenteExperimentalSchema import FuenteExperimentalSchema                                         
from models.mongo.jaula import Jaula
from schemas.animalSchema import NuevoAnimalSchema,AsignarAnimalAJaula

class AnimalService:
    @classmethod
    def find_by_id(cls, idAnimal):
        return FuenteExperimental.objects(id_fuenteExperimental = idAnimal).first()
    
    #Agregar validaciones
    @classmethod
    def nuevoAnimal(cls, datos):
        animal = NuevoAnimalSchema().load(datos)
        animal.tipo = 'Animal'
        animal.id_proyecto = cls.validarJaula(animal.id_jaula)
        animal.save()
    
    @classmethod
    def asignarJaulaAAnimales(cls, datos):
        animales = AsignarAnimalAJaula().load(datos, many=True)
        cls.validarJaula(animales[0].id_jaula)
        for animal in animales:
            _id_proyecto = cls.validarJaula(animal.id_jaula)
            FuenteExperimental.objects(id_fuenteExperimental =  animal.id_fuenteExperimental).update(id_jaula = animal.id_jaula, id_proyecto = _id_proyecto )
    
    def validarJaula(idJaula):
        from .jaulaService import JaulaService
        return JaulaService.find_by_id(idJaula).id_proyecto

    @classmethod
    def todosLosAnimales(cls):
        return FuenteExperimental.objects(tipo ="Animal", baja=False).all()

    @classmethod
    def animalesSinJaula(cls):
        return FuenteExperimental.objects(id_jaula = 0, tipo="Animal", codigoGrupoExperimental__ne="", baja=False).all()

    @classmethod
    def animalesDeLaJaula(cls, idJaula):
        return  FuenteExperimental.objects(id_jaula = idJaula).all()

    @classmethod
    def bajarAnimal(cls, idAnimal):
        animal = FuenteExperimental.objects(id_fuenteExperimental = idAnimal)
        if animal:
            return FuenteExperimental.objects(id_fuenteExperimental = idAnimal).update(
                baja = True,
                id_jaula = 0
                )
        return None
    
    @classmethod
    def animalesDelProyecto(cls, idProyecto):
        #codigoGrupoExperimental__ne=""
        return FuenteExperimental.objects(codigoGrupoExperimental='',id_proyecto = idProyecto,  tipo ="Animal", codigo='',baja=False).all()

    @classmethod
    def actualizarProyectoAnimalesDeJaulas(cls,jaula):
        FuenteExperimental.objects(id_jaula = jaula.id_jaula).update(set__id_proyecto =jaula.id_proyecto)


