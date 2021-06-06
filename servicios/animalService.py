from models.mongo.fuenteExperimental import AnimalSchema, FuenteExperimental, FuenteExperimentalSchema, NuevoAnimalSchema
from models.mongo.jaula import Jaula

class AnimalService:

    @classmethod
    def find_by_id(cls, idAnimal):
        animal = FuenteExperimental.objects(id_jaula = idAnimal).first()
        if animal:
            return animal.json()
        return None
    
    @classmethod
    def nuevoAnimal(cls, datos):
        animal = NuevoAnimalSchema().load(datos)
        animal.tipo = 'Animal'
        animal.save()
    
    @classmethod
    def asignarJaulaAAnimales(cls, datos):
        animales = AnimalSchema().load(datos, many=True)
        print(animales)
        errores = []
        for animal in animales:
            if cls.existeLaJaulas(animal.id_jaula):
                FuenteExperimental.objects(id_fuenteExperimental =  animal.id_fuenteExperimental).update(id_jaula = animal.id_jaula)
            else:
                errores.append({"Error" : f"No se pudo asignar el animal con el id {animal.id_fuenteExperimental} a la jaula con el id {animal.id_jaula}. El id de la jaula debe ser uno válido y debe estar habilitada."})
        return errores
    
    @classmethod
    def existeLaJaulas(cls, idJaula):
        jaula = Jaula.objects(id_jaula = idJaula, habilitado = True).first()
        return jaula != None

    @classmethod
    def todosLosAnimales(cls):
        return AnimalSchema().dump(FuenteExperimental.objects(codigoGrupoExperimental = "", tipo ="Animal", baja=False).all(), many=True)
    
    @classmethod
    def animalesSinJaula(cls):
        return AnimalSchema().dump(FuenteExperimental.objects(id_jaula = 0, tipo ="Animal", baja=False).all(), many=True)

    @classmethod
    def animalesDeLaJaula(cls, idJaula):
        animales = FuenteExperimental.objects(id_jaula = idJaula).all()
        return FuenteExperimentalSchema().dump(animales, many=True)

    @classmethod
    def bajarAnimal(cls, idAnimal):
        animal = FuenteExperimental.objects(id_fuenteExperimental = idAnimal)
        if animal:
            return FuenteExperimental.objects(id_fuenteExperimental = idAnimal).update(
                baja = True,
                id_jaula = 0
                )
        return None