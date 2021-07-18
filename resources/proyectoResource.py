from flask_restful import Resource
from flask_jwt import jwt_required
from flask import  request
from marshmallow import ValidationError
from exceptions.exception import ErrorExpDeProyecto,ErrorExperimentoInexistente,ErrorUsuarioInexistente,ErrorProyectoInexistente,ErrorJaulaInexistente,ErrorJaulaDeProyecto
from schemas.proyectoSchema import ProyectoSchema
from servicios.proyectoService import ProyectoService
from servicios.commonService import CommonService
from schemas.usuarioSchema import UsuarioSchema
from schemas.blogSchema import BlogSchema

class Proyectos(Resource):
    #@jwt_required()
    def get(self):
        return CommonService.jsonMany(ProyectoService.find_all(),ProyectoSchema)

class NuevoProyecto(Resource):
    # @jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.nuevoProyecto(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except ErrorUsuarioInexistente as err:
                return {'Error':err.message},400
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
        try:
            proyecto = ProyectoService.find_by_id(id_proyecto)
            return CommonService.json(proyecto,ProyectoSchema),200
        except ErrorProyectoInexistente as err:
            return {'error': err.message}, 400

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
        try:
            usuarios=  ProyectoService.obtenerMiembrosProyecto(id_proyecto)
            return  CommonService.jsonMany(usuarios,UsuarioSchema)
        except ValidationError as err:
            return {'error': err.messages}, 400
        except ErrorProyectoInexistente as err:
            return {'error': err.message}, 400

class ObtenerBlogsProyecto(Resource):
    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return ProyectoService.obtenerBlogsProyecto(datos)
                return CommonService.jsonMany(blogs,BlogSchema)
            except ValidationError as err:
                return {'error': err.messages}, 400
            except ErrorProyectoInexistente as err:
                return {'Error':err.message},400
        return {"Status" : "Deben indicarse datos para el blog"}, 400

class NuevoBlogProyecto(Resource):
    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.nuevoBlogsProyecto(datos)
                return {'Status':'ok'}, 200
            except ValidationError as err:
                return {'error': err.messages}, 400
            except (ErrorProyectoInexistente,ErrorJaulaInexistente,
            ErrorJaulaDeProyecto,ErrorExperimentoInexistente,ErrorExpDeProyecto) as err:
                return {'Error':err.message},400 
        return {"Status" : "Deben indicarse datos para el blog"}, 400