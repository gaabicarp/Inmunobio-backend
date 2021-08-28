from copy import error
from re import I
from servicios.commonService import CommonService
from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from schemas.animalSchema import AnimalSchema
from servicios.animalService import AnimalService

class Animal(Resource):
    def get(self, idAnimal):
        if idAnimal:
            animal = AnimalService().find_by_id(idAnimal)
            return  CommonService.json(animal,AnimalSchema)
        return {'Error' : f"El id {idAnimal} no es válido."}, 400

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                AnimalService().nuevoAnimal(datos)
                return {'Status':'Se creó el nuevo animal.'}, 200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': 'Se deben enviar datos para la creación del animal.'},400

    def put(self, idAnimal):
        if idAnimal:
            if AnimalService().bajarAnimal(idAnimal):
                return {'Status': f'Se dio de baja el animal con id {idAnimal}'}
            return {'Status': f'No se encontró ningún animal con el id {idAnimal}'}, 200
        return {'Error' : f"El id {idAnimal} no es válido."}, 400


class Animales(Resource):

    #@jwt_required()
    def get(self):
        return CommonService.jsonMany(AnimalService().todosLosAnimales(),AnimalSchema)

class AnimalesSinJaula(Resource):

    def get(self):
        animales = AnimalService.animalesSinJaula()
        if animales:
            return animales, 200
        return {'Status': 'No se encontraron animales sin jaula.'}, 200

class AnimalesDeLaJaula(Resource):

    def get(self, idJaula):
        if idJaula:
            animales = AnimalService().animalesDeLaJaulaSchema(idJaula)
            if animales:
                return animales, 200
            return {'Status': f'No se encontraron animales para el id {idJaula} de la jaula.'}, 200
        return {'Error': 'Se debe indicar un id de la jaula.'}, 400

    def put(self):
        datos = request.get_json()
        if datos:
            #try:
            AnimalService().asignarJaulaAAnimales(datos)
            return {'Status': 'Se asignaron los animales a la jaula.'}, 200
                #return ({'Status': 'Se asignaron los animales a la jaula.'}, 200) if len(errores) == 0 else ({"Status": errores}, 400)
            #except Exception as err:
            #   return {'Error' : err.args}, 400
            #  print("hola")
        return {'Error' : "Se deben enviar un array de aniamles."}, 400

class AnimalesProyecto(Resource):

    def get(self, idProyecto):
        if idProyecto:
            return CommonService.jsonMany(AnimalService().animalesDelProyecto(idProyecto),AnimalSchema)
        return {'Error' : "Se debe indicar un id del proyecto"}, 400