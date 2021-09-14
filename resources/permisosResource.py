from servicios.permisosService import PermisosService
from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request

class Permisos(Resource):
    #get all 
    def get(self):
        return  PermisosService.all_permisos()

class ObtenerPermisoPorId(Resource):
    def get(self,id_permiso):
       return PermisosService.obtenerPermisoPorId(id_permiso)
