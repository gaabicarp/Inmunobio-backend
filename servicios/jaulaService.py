from flask.json import dump
from models.mongo.jaula import Jaula, JaulaSchema, NuevaJaulaSchema, ActualizarProyectoJaulaSchema, ActualizarJaulaSchema
from servicios.fuenteExperimentalService import FuenteExperimentalService
from dateutil import parser

class JaulaService:

    @classmethod
    def find_by_id(cls, idJaula):
        return Jaula.objects(id_jaula = idJaula).first()
    
    @classmethod
    def jaulasSinAsignar(cls):
        jaulas = Jaula.objects(id_proyecto = 0).all()
        if jaulas:
            return JaulaSchema().dump(jaulas, many=True)
        return None
    
    @classmethod
    def jaulasDelProyecto(cls, idProyecto):
        jaulas = Jaula.objects(id_proyecto = idProyecto).all()
        if jaulas:
            return JaulaSchema().dump(jaulas, many=True)
        return None

    @classmethod
    def crearJaula(cls, datos):
        jaula = NuevaJaulaSchema().load(datos)
        jaula.save()
    
    @classmethod
    def actualizarProyectoDeLaJaula(cls, datos):
        jaula = ActualizarProyectoJaulaSchema().load(datos)
        Jaula.objects(id_jaula = jaula.id_jaula).update(
            id_proyecto = jaula.id_proyecto,
            nombre_proyecto = jaula.nombre_proyecto
        )

    @classmethod
    def actualizarJaula(cls, datos):
        jaula = ActualizarJaulaSchema().dump(datos)
        Jaula.objects(id_jaula = jaula.id_jaula).update(
            codigo = jaula.codigo,
            rack = jaula.rack,
            estante = jaula.estante,
            capacidad = jaula.capacidad,
            tipo = jaula.tipo
        )
    
    @classmethod
    def bajarJaula(cls, idJaula):
        jaula = Jaula.objects(id_jaula = idJaula).first()
        if jaula:
            if not cls.laJualaTieneAnimales(cls, idJaula):
                Jaula.objects(id_jaula = idJaula).update(habilitado = False)
                return {'Status':'Ok'}, 200
            else:
                return {'Status':'La jaula debe estar vacía para poder darla de baja'}, 400
        return {'Status': f'No se encontró una jaula con el id {idJaula}.'}, 200

    def laJualaTieneAnimales(self, idJaula):
        animales = FuenteExperimentalService.animalesDeLaJaula(idJaula)
        return  len(animales) > 0
