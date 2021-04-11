from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError

from models.mongo.experimento import Experimento, ExperimentoSchema, AltaExperimentoSchema, CerrarExperimentoSchema

class Experimentos(Resource):

    #@jwt_required()
    def get(self, idProyecto):
        if idProyecto:
            experimentos = Experimento.find_all_by_idProyecto(idProyecto)
            return experimentos, 200
        return {"Error:" "Se debe indicar un id del proyecto válido"}, 400

class ExperimentoResource(Resource):

    #@jwt_required()
    def get(self, idExperimiento):
        if idExperimiento:
            experimento = Experimento.find_by_id(idExperimiento)
            if experimento:
                return experimento.json(), 200
            return {f"Status:":"No se encontraron resultados con el id_experimento {idExperimento}"}, 204
        return {"Error:" "Se debe indicar un id de experimento válido"}, 400

    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                nuevoExperimento = AltaExperimentoSchema().load(datos)
                nuevoExperimento.save()
                return {"Status":"ok"}, 201
            except ValidationError as err:
                return {'error': err.messages},400
        return {"Error:" "Se deben enviar datos para la creación del experimento"}, 400

"""     #@jwt_required()
    def put(self, idExperimiento):
        datos = request.get_json()
        if idExperimiento and datos:
            Experimento.update_experimento(datos)
            return {"Status": "OK"}, 200
        return {"Error:" "Se deben enviar datos para la actualización del experimento"}, 400 """