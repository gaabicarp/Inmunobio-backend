from models.mongo.fuenteExperimental import AnimalSchema, FuenteExperimental, FuenteExperimentalSchema, NuevoAnimalSchema
from models.mongo.jaula import Jaula
from .validationService import Validacion

class AnimalService:

    @classmethod
    def find_by_id(cls, idAnimal):
        animal = FuenteExperimental.objects(id_jaula = idAnimal).first()
        if animal:
            return animal.json()
        return None
    
    #Agregar validaciones
    @classmethod
    def nuevoAnimal(cls, datos):
        animal = NuevoAnimalSchema().load(datos)
        animal.tipo = 'Animal'
        cls.validarJaula(animal.id_jaula)
        animal.save()
    
    @classmethod
    def asignarJaulaAAnimales(cls, datos):
        animales = AnimalSchema().load(datos, many=True)
        print(animales)
        cls.validarJaula(animales[0].id_jaula)
        for animal in animales:
            FuenteExperimental.objects(id_fuenteExperimental =  animal.id_fuenteExperimental).update(id_jaula = animal.id_jaula)
    
    def validarJaula(idJaula):
        if not Validacion.existeLaJaulas(idJaula):
            raise Exception(f"No existe la jaula con id {idJaula} o no se encuentra habilitada.")


    @classmethod
    def todosLosAnimales(cls):
        return AnimalSchema().dump(FuenteExperimental.objects(codigoGrupoExperimental__ne="", tipo ="Animal", baja=False).all(), many=True)
    
    @classmethod
    def animalesSinJaula(cls):
        return AnimalSchema().dump(FuenteExperimental.objects(id_jaula = 0, tipo="Animal", codigoGrupoExperimental__ne="", baja=False).all(), many=True)

    @classmethod
    def animalesDeLaJaula(cls, idJaula):
        return  FuenteExperimental.objects(id_jaula = idJaula).all()

    @classmethod
    def animalesDeLaJaulaSchema(cls, idJaula):
        return AnimalSchema().dump(cls.animalesDeLaJaula(idJaula), many=True)

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
        animales = FuenteExperimental.objects(id_proyecto = idProyecto, codigoGrupoExperimental__ne="", tipo ="Animal", baja=False).all()
        if animales:
            return AnimalSchema().dump(animales, many=True)
        return None