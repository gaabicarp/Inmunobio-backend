from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError

from servicios.experimentoService import ExperimentoService

class Experimentos(Resource):

    #@jwt_required()
    def get(self, idProyecto):
        if idProyecto:
            experimentos = ExperimentoService().find_all_by_idProyecto(idProyecto)
            return experimentos, 200
        return {"Error" : "Se debe indicar un id del proyecto válido."}, 400

class ExperimentoResource(Resource):

    #@jwt_required()
    def get(self, idExperimiento):
        if idExperimiento:
            experimento = ExperimentoService().find_by_id(idExperimiento)
            if experimento:
                return experimento.json(), 200
            return {f"Status:":"No se encontraron resultados con el id_experimento {idExperimento}."}, 204
        return {"Error" : "Se debe indicar un id de experimento válido."}, 400

    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.nuevoExperimento(datos)
                return {"Status":"ok"}, 201
            except ValidationError as err:
                return {'error': err.messages},400
        return {"Error" : "Se deben enviar datos para la creación del experimento."}, 400

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.modificarExperimento(datos)
                return {"Status":"ok"}, 201
            except ValidationError as err:
                return {'Error': err.messages},400
        return {"Error" : "Se deben enviar datos para la actualización del experimento."}, 400

class CerrarExperimento(Resource):

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.cerrarExperimento(datos)
                return {"Status" : "ok"}
            except ValidationError as err:
                return {'Error': err.messages},400
        return {"Error" : "Se deben enviar datos para poder cerrar el experimento."}, 400

class ExperimentoMuestra(Resource):

    #@jwt_required()
    def put(self, datos):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.agregarMuestrasExternasAlExperimento(datos)
                return {"Status" : "Ok"}, 200
            except ValidationError as err:
                return {"Error" : err.messages}, 400
            except Exception as err:
                return {"Error" : str(err)}, 400
        return {"Error" : "Se deben enviar datos para poder agregar muestras."}, 400
