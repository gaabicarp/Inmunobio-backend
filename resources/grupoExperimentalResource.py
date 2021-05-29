from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError

from servicios.grupoExperimentalService import GrupoExperimentalService

class GrupoExperimental(Resource):

    def get(self, idGrupoExperimental):
        if idGrupoExperimental:
            grupoExperimental = GrupoExperimentalService().find_by_id(idGrupoExperimental)
            return grupoExperimental, 200
        return {"Error" : "Se debe indicar el id del grupo experimental"}

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoExperimentalService().CrearGrupoExperimental(datos)
                return {"Status": "OK"}, 200
            except ValidationError as err:
                return {"Error" : err.messages}, 400
        return {"Error" : "Se deben enviar datos para la creación de un grupo experimental"}, 400

class GruposExperimentales(Resource):

    def get(self, idExperimento):
        if idExperimento:
            gruposExperimentales = GrupoExperimentalService().gruposExperimentalesDelExperimento(idExperimento)
            if gruposExperimentales:
                return gruposExperimentales, 200
            else:
                return {f"Status" : "No se encontraron grupos experimentales para el experimento {idExperimento}"}, 204
        return {"Error" : "Se debe enviar un id del experimento"}, 400
