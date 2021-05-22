from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError

from servicios.jaulaService import JaulaService

class Jaula(Resource):

    def get(self, idJaula):
        if idJaula:
            jaula = JaulaService().find_by_id(idJaula)
            if jaula:
                return jaula.json(), 200
            else:
                return {"Status" :  f"No se encontró ninguna jaula con el id: {idJaula}"}, 200
        return {"Error" : "Se debe indicar el id de una jaula."}, 400


    def post(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.crearJaula(datos)
                return {"status": "Jaula creada."}, 200
            except ValidationError as err:
                return {'Error': err.messages},400
        return  {'Error':'Se deben enviar datos para la creación de la jaula.'},404

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.actualizarProyectoDeLaJaula(datos)
                return {"status" : "Se asignó la jaula al proyecto"}, 200
            except ValidationError as err:
                return {"Error" : err.messages}, 400
        return  {'Error':'Se deben enviar datos para la modificación de la jaula.'},404

    def delete(self, idJaula):
        if idJaula:
            return JaulaService.bajarJaula(idJaula)
        return {'Error': 'Se debe indicar un id para la jaula.'}, 400

class JaulasSinProyecto(Resource):

    def get(self):
        jaulas = JaulaService.jaulasSinAsignar()
        if jaulas:
            return jaulas, 200
        else:
            return {"Status" : "No hay jaulas disponibles."}, 200

class JaulasDelProyecto(Resource):

    def get(self, idProyecto):
        jaulas = JaulaService.jaulasDelProyecto(idProyecto)
        if jaulas:
            return jaulas, 200
        else:
            return {"Status" : "No hay jaulas asignadas a ese proyecto."}, 200