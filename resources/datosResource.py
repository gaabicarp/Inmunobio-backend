from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from servicios.datosService import DatosService

class DatosResourceMongo(Resource):
    #@jwt_required()
    def post(self):
        datos = request.get_json()
        try:
            DatosService.llenarBase(datos)
            return  {'ok': 'Todo salio bien n.n '}, 200
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as err:
            return {'Error': str(err)}, 400

class DatosResourceMysql(Resource):
    #@jwt_required()
    def post(self):
        datos = request.get_json()
        try:
            DatosService.llenarBaseMysql(datos)
            return  {'ok': 'Todo salio bien n.n '}, 200
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as err:
            return {'Error': str(err)}, 400