from servicios.permisosService import PermisosService
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import request

class Permisos(Resource):
    #get all 
    def get(self):
        return  PermisosService.all_permisos()

class ObtenerPermisoPorId(Resource):
    def get(self):
        datos = request.get_json()
        if (datos):
            return PermisosService.obtenerPermisoPorId(datos)
        return {'name': 'None'},404
