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
        usuarios = UsuarioService.findUsuariosHabilitados()
        if usuarios:
           return UsuarioService.jsonMany(usuarios) 
        return {'name': 'None'},400
        
class ModificarUsuario(Resource): 
    #@jwt_required()
    def put(self):
        ''' recibe: un idUsuario y/o direccion y/o telefono y/o mail y/o contraseña en formato json.
        Modifica esos campos de un usuario si existe.
        devuelve: solo mensajes de status.
        '''
        datos = request.get_json()
        if (datos):
            #ver para que se verifique con schema que exista id_usuario en json
            usuario = UsuarioService.find_by_id(datos['id_usuario'])
            if (usuario):
                print("entra al if de datos y usuario")
                return UsuarioService.modificarUsuario(usuario,datos)
            return {'error':'No existe usuario'},400
        return {'name': 'None'},400

    def delete(self):
        '''recibe una id de usuario si este esta habilitado lo deshabilita'''
        datos = request.get_json()
        if datos:
                return UsuarioService.deshabilitarUsuario(datos)
        return {'name': 'None'},400

class BusquedaPorID(Resource):
 #@jwt_required()
    def get(self,id_usuario):
        ''' recibe: un idUsuario como parametro
            devuelve: el usuario,si hay match con esa id y ademas esta habilitado, 
           en formato json.
        '''
        usuario = UsuarioService.find_by_id(id_usuario)
        if usuario:
                return UsuarioService.json(usuario)
        return {'error':'No existe el usuario'},400
   

class NuevoUsuario(Resource):
   # @jwt_required()
    def post(self):
        datos = request.get_json()
        if (datos ):
          return UsuarioService.nuevoUsuario(datos)
        return {'name': 'None'},400
     

class ActualizarPermisos(Resource):
    '''dado un id de usuario y una lista con dic de permisos , actualiza los permisos
    del usuario con dicha lista'''
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if(datos):
            return UsuarioService.actualizarPermisos(datos)
        return {'name': 'None'}, 400

class ObtenerUsuariosParaProyecto(Resource):
    #aca el 4 representa la id del permiso director de proyecto,ya que no hay visibilidad
    #entre un director de proyecto y otro con mismo permiso.
    def get(self):
       return UsuarioService.usuariosSinElPermiso(4)



