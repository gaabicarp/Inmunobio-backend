from servicios.usuarioService import UsuarioService
from servicios.permisosService import PermisosService
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify, request
from db import db
import json

class Usuarios(Resource):
    '''devuelve todos los usuarios de la base que se encuentren habilitados 
    '''
    def get(self):
        usuarios = UsuarioService.find_usuarios_Habilitados()
        if usuarios:
           return UsuarioService.jsonMany(usuarios) 
        return {'name': 'None'},404
        
class UsuariosXIdUsuario(Resource):
    #@jwt_required()
    def get(self):
        ''' recibe: un idUsuario en formato json
            devuelve: el usuario,si hay match con esa id y ademas esta habilitado, 
           en formato json.
        '''
        datos = request.get_json()
        if datos:
            usuario = UsuarioService.busquedaValidada(datos)
            if usuario:
                return UsuarioService.json(usuario)
            return {'error':'No existe el usuario'}
        return {'name': 'None'},404
    
    #@jwt_required()
    def put(self):
        ''' recibe: un idUsuario y/o direccion y/o telefono y/o mail y/o contraseña en formato json.
        Modifica esos campos de un usuario si existe.
        devuelve: solo mensajes de status.
        '''
        modificaciones = request.get_json()
        if (modificaciones):
            usuario = UsuarioService.busquedaValidada(modificaciones)
            if (usuario):
                return UsuarioService.modificarUsuario(usuario,modificaciones)
            return {'error':'No existe usuario'},404
        return {'name': 'None'},404

    def delete(self):
        '''recibe una id de usuario si este esta habilitado lo deshabilita'''
        datos = request.get_json()
        if datos:
                return UsuarioService.deshabilitarUsuario(datos)
        return {'name': 'None'},404
    
class NuevoUsuario(Resource):
   # @jwt_required()
    def post(self):
        datos = request.get_json()
        if (datos ):
          return UsuarioService.nuevoUsuario(datos)
        return {'name': 'None'},404
     

class ActualizarPermisos(Resource):
    '''dado un id de usuario y una lista con dic de permisos , actualiza los permisos
    del usuario con dicha lista'''
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if(datos):
            print("if de datos ok")
            return UsuarioService.actualizarPermisos(datos)
        return {'name': 'None'}, 404

class ObtenerUsuariosParaProyecto(Resource):
    #aca el 4 representa la id del permiso director de proyecto,ya que no hay visibilidad
    #entre un director de proyecto y otro con mismo permiso.
    def get(self):
       return UsuarioService.usuariosSinElPermiso(4)



