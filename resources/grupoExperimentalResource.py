from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from servicios.commonService import CommonService
from servicios.grupoExperimentalService import GrupoExperimentalService
from schemas.grupoExperimentalSchema import GrupoExperimentalSchema, AltaGrupoExperimentalSchema, DividirGrupoExperimentalSchema,AgregarFuentesAlGrupoExperimentalSchema

class GrupoExperimental(Resource):

    def get(self, idGrupoExperimental):
        if idGrupoExperimental:
            return  CommonService.json(GrupoExperimentalService().find_by_id(idGrupoExperimental),GrupoExperimentalSchema) 
        return {"Error" : "Se debe indicar el id del grupo experimental"}

    def delete(self, idGrupoExperimental):
        if idGrupoExperimental:
            GrupoExperimentalService().borrarGrupoExperimental(idGrupoExperimental)
            return  {"Status" : "Se borró el grupo experimental y sus subgrupos."}, 200
        return {"Error" : "Se debe indicar el id del grupo experimental"}

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoExperimentalService().CrearGrupoExperimental(datos)
                return {"Status": "Se creó el grupo experimental"}, 200
            except Exception as err:
                return {"Error" : str(err)}, 400
        return {"Error" : "Se deben enviar datos para la creación de un grupo experimental"}, 400

class GruposExperimentales(Resource):
    def get(self, idExperimento):
        if idExperimento:
            return CommonService.jsonMany(GrupoExperimentalService().gruposExperimentalesDelExperimento(idExperimento), GrupoExperimentalSchema) 
        return {"Error" : "Se debe enviar un id del experimento"}, 400

class DividirGrupoExperimental(Resource):

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                GrupoExperimentalService().dividirGrupoExperimental(datos)
                return {"Status" : "Ok"}, 200
            except Exception as err:
                return {"Error" : str(err)}, 400
            except ValidationError as err:
                return {"Error" : err.messages}, 400
        return {"Error" : "Se deben enviar datos para la división de un grupo experimental"}, 400
