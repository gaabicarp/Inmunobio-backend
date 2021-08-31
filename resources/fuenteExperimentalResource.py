from flask_restful import Resource
from flask import request
from servicios.fuenteExperimentalService import FuenteExperimentalService
from servicios.commonService import CommonService
from schemas.fuenteExperimentalSchema import FuenteExperimentalSchema

class FuenteExperimental(Resource):
    def get(self, codigo):
        if codigo:
            try:
                fuenteExperimental = FuenteExperimentalService.find_by_codigo(codigo)
                return CommonService.json(FuenteExperimentalSchema,fuenteExperimental)
            except Exception as err:
                return {'error': err.args}, 400
        return {'Error': 'Es necesario indicar el codigo de la fuente experimental.'}, 400

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                FuenteExperimentalService.nuevasFuentesExperimentales(datos)
                return {"Status" : "Se crearon las fuentes experimentales"}, 200
            except Exception as err:
                return {"Error" : err.args}, 400
        return {'Error' : "Se deben enviar datos para la creación de la fuente experimental."}, 400

class FuentesExperimentalesPorId(Resource):
    def get(self, id_fuente):
        if id_fuente:
            try:
                fuenteExperimental = FuenteExperimentalService.find_by_id(id_fuente)
                return CommonService.json(fuenteExperimental,FuenteExperimentalSchema)
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Es necesario indicar el id de la fuente experimental.'}, 400

class FuentesExperimentalesPorProyecto(Resource):
    def get(self, id_proyecto):
        if id_proyecto:
            try:
                fuentesExperimentales = FuenteExperimentalService.find_by_proyecto(id_proyecto)
                return CommonService.jsonMany(fuentesExperimentales,FuenteExperimentalSchema)
            except Exception as err:
                return {'error': err.args}, 400
        return {'Error': 'Es necesario indicar el id del proyecto al que pertenecn las fuentes experimentales.'}, 400
