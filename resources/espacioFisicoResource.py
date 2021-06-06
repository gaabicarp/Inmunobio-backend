from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.espacioFisicoService import EspacioFisicoService


class EspacioFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().altaEspacioFisico(datos)
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(datos)
        return {'name': 'None'},400

class EspacioFisicoID(Resource):
    def get(self,id_espacioFisico):
        return EspacioFisicoService().obtenerEspacio(id_espacioFisico)

    def delete(self,id_espacioFisico):
        if(id_espacioFisico):
            return EspacioFisicoService().borrarEspacio(id_espacioFisico)
        return {'name': 'None'},400
        
class CrearBlogEspacioFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(datos)
        return {'name': 'None'},400

class BorrarBlogEspacioFisico(Resource):
    def delete(self,id_espacioFisico,id_blog):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(id_espacioFisico,id_blog)
        return {'name': 'None'},400

   