from flask_restful import Resource
from flask import request
from servicios.grupoExperimentalService import GrupoExperimentalService


class GrupoExperimental(Resource):

    def get(self, idGrupoExperimental):
        if idGrupoExperimental:
            try:
                return GrupoExperimentalService().obtenerGrupoPorId(idGrupoExperimental)
            except Exception as err:
                return {"Error" : err.args}, 400
        return {"Error" : "Se debe indicar el id del grupo experimental"}

    def delete(self, idGrupoExperimental):
        if idGrupoExperimental:
            try:
                GrupoExperimentalService().borrarGrupoExperimental(idGrupoExperimental)
                return  {"Status" : "Se borró el grupo experimental y sus subgrupos."}, 200
            except Exception as err:
                return {"Error" : err.args}, 400
        return {"Error" : "Se debe indicar el id del grupo experimental"}

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoExperimentalService().CrearGrupoExperimental(datos)
                return {"Status": "Se creó el grupo experimental"}, 200
            except Exception as err:
                return {"Error" : err.args}, 400
        return {"Error" : "Se deben enviar datos para la creación de un grupo experimental"}, 400

class GruposExperimentales(Resource):
    def get(self, idExperimento):
        if idExperimento:
            return GrupoExperimentalService().obtenerGruposExperimentalesDelExperimento(idExperimento)
        return {"Error" : "Se debe enviar un id del experimento"}, 400

class DividirGrupoExperimental(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoExperimentalService().dividirGrupoExperimental(datos)
                return {"Status" : "Se dividio el grupo experimental."}, 200
            except Exception as err:
                return {"Error": err.args}, 400
        return {"Error" : "Se deben enviar datos para la división de un grupo experimental"}, 400
