from flask_restful import Resource
from flask_jwt import jwt_required
from flask import  request
from marshmallow import ValidationError

from servicios.proyectoService import ProyectoService

class Proyectos(Resource):

    #@jwt_required()
    def get(self):
        proyectos = ProyectoService.find_all()
        if proyectos:
           return proyectos 
        return {'name': 'None'},404

class NuevoProyecto(Resource):

    # @jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.nuevoProyecto(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},404
        return {'name': datos},404

class CerrarProyecto(Resource):
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.cerrarProyecto(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},404
        return {'name': datos},404

class ProyectoID(Resource):
    #@jwt_required()
    def get(self, id_proyecto):
        proyecto = ProyectoService.find_by_id(id_proyecto)
        if proyecto:
            return ProyectoService.json(proyecto), 200

class ModificarProyecto(Resource):
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.modificarProyecto(datos)
                return {'Status':'ok'}, 200
            except ValidationError as err:
                return {'error': err.messages}, 400
        return {'name': datos}, 400

class ObtenerUsuariosProyecto(Resource):
    #@jwt_required()
    def get(self,id_proyecto):
        datos = request.get_json()
        if datos:
            try:
                return ProyectoService.obtenerMiembrosProyecto(id_proyecto)
            except ValidationError as err:
                return {'error': err.messages}, 400
        return {'name': datos}, 400
