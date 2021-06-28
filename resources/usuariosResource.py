from warnings import catch_warnings
from servicios.usuarioService import UsuarioService
from flask_restful import Resource,Api
from flask import request
#from exceptions.exception import ErrorUsuariosInexistentes
from servicios.validationService import ValidacionesUsuario
from exceptions.exception import ErrorPermisoInexistente,ErrorUsuarioInexistente
from marshmallow import ValidationError
from servicios.commonService import CommonService
from schemas.usuarioSchema import UsuarioSchema

class ObtenerUsuariosResource(Resource):
    '''devuelve todos los usuarios de la base que se encuentren habilitados 
    '''
    def get(self):
            return UsuarioService.findUsuariosHabilitados() 

class UsuarioResource(Resource): 
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if (datos):
            try:
                UsuarioService.modificarUsuario(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except (ErrorUsuarioInexistente,ErrorPermisoInexistente) as err:
                return {'Error': err.message},400
        return {'name': 'None'},400
       
    # @jwt_required()
    def post(self):
        datos = request.get_json()
        if (datos):
            try:
                UsuarioService.nuevoUsuario(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except ErrorPermisoInexistente as err:
                return {'error': err.message},400
        return {'name': 'None'},400

class UsuarioID(Resource):
 #@jwt_required()
    def get(self,id_usuario):
        ''' recibe: un idUsuario como parametro
            devuelve: el usuario,si hay match con esa id y ademas esta habilitado, 
           en formato json.'''
        if(id_usuario):
            try:
                usuario = UsuarioService.find_by_id(id_usuario)
                return CommonService.json(usuario,UsuarioSchema)
            except ErrorUsuarioInexistente as err:
                return {'Error': err.message},400
        return {'name': 'None'},400
 
    def delete(self,id_usuario):
        '''recibe una id de usuario si este esta habilitado lo deshabilita'''
        try:
            UsuarioService.deshabilitarUsuario(id_usuario)  
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorUsuarioInexistente as err:
            return {'Error':err.message},400

class ObtenerUsuariosParaProyecto(Resource):
    #aca el 4 representa la id del permiso director de proyecto,ya que no hay visibilidad
    #entre un director de proyecto y otro con mismo permiso.
    def get(self):
       return UsuarioService.usuariosSinElPermiso(4)



