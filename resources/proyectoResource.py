from flask_restful import Resource
from flask_jwt import jwt_required
from flask import  request
from schemas.proyectoSchema import ProyectoExtendido
from servicios.proyectoService import ProyectoService
from servicios.commonService import CommonService
from schemas.usuarioSchema import UsuarioSchema

class Proyectos(Resource):
    #@jwt_required()
    def get(self):
        try:
            return CommonService.jsonMany(ProyectoService.find_all(),ProyectoExtendido)
        except Exception as err:
            return {'Error': err.args},400

class NuevoProyecto(Resource):
    # @jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.nuevoProyecto(datos)
                return {'Status':'El proyecto fue dado de alta.'},200
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben suministrarse datos para el alta del proyecto.'},404

class CerrarProyecto(Resource):
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.cerrarProyecto(datos)
                return {'Status':'El proyecto cambió a estado finalizado.'},200
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Debe suministrar los datos del proyecto a cerrar.'},404

class ProyectoID(Resource):
    #@jwt_required()
    def get(self, id_proyecto):    
        if(id_proyecto):
            try:
                return  CommonService.json(ProyectoService.obtenerProyecto(id_proyecto),ProyectoExtendido),200
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben indicarse id del proyecto'}, 400

class ModificarProyecto(Resource):
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.modificarProyecto(datos)
                return {'Status':'Proyecto modificado.'}, 200
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben indicarse datos para la modificacion del proyecto'}, 400

class ObtenerUsuariosProyecto(Resource):
    #@jwt_required()
    def get(self,id_proyecto):
        if(id_proyecto):
            try:
                return  CommonService.jsonMany(ProyectoService.obtenerMiembrosProyecto(id_proyecto),UsuarioSchema)
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben indicarse id del proyecto'}, 400

class ObtenerBlogsProyecto(Resource):
    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return ProyectoService.obtenerBlogsProyecto(datos)
            except Exception as err:
                return {'Error': err.args},400
        return {"Error" : "Deben indicarse datos para el blog"}, 400

class NuevoBlogProyecto(Resource):
    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ProyectoService.nuevoBlogsProyecto(datos)
                return {'Status':'Se creó el blog de proyecto.'}, 200
            except Exception as err:
                return {'Error': err.args},400
        return {"Error" : "Deben indicarse datos para el blog"}, 400

class ObtenerProyectoDeUsuario(Resource):
    #Devuelve proyectos donde es jefe y en los que participa.
    #@jwt_required()
    def get(self,id_usuario):
        if(id_usuario):
            try:
                return  CommonService.jsonMany(ProyectoService.obtenerProyectosUsuario(id_usuario),ProyectoExtendido)
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben indicarse id de usuario'}, 400