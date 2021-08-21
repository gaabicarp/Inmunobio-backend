from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.fuenteExperimentalService import FuenteExperimentalService

class FuenteExperimental(Resource):

    def get(self, codigo):
        if codigo:
            fuenteExperimental = FuenteExperimentalService.find_by_codigo(codigo)
            if fuenteExperimental:
                return fuenteExperimental, 200
            else:
                return {"Status" : f"No se encontró una fuente experimental para el id {codigo}"}, 200
        return {'Error': 'Es necesario indicar el id de la fuente experimental.'}, 400

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return FuenteExperimentalService.nuevasFuentesExperimentales(datos)
            except Exception as err:
                return {"Error" : err.args}, 400
        return {'Error' : "Se deben enviar datos para la creación de la fuente experimental."}, 400

class FuentesExperimentales(Resource):
    def get(self):
        pass


#fuente experimental x id 

#fuentes experimentales de proyecto