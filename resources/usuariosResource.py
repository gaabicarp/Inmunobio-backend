import datetime
from re import U
from schemas.usuarioSchema import UsuarioSchema
from servicios.commonService import CommonService
from warnings import catch_warnings
from servicios.usuarioService import UsuarioService
from flask_restful import Resource,Api
from flask import request
from werkzeug.security import check_password_hash
from flask_jwt import jwt
from flask import jsonify
from servicios.validationService import ValidacionesUsuario
from exceptions.exception import ErrorPermisoGeneral,ErrorPermisoInexistente,ErrorUsuarioInexistente,ErrorUsuarioExistente
from marshmallow import ValidationError, exceptions
from servicios.commonService import CommonService

class ObtenerUsuariosResource(Resource):
    '''devuelve todos los usuarios de la base que se encuentren habilitados 
    '''
    def get(self):
            return CommonService.jsonMany(UsuarioService.findUsuariosHabilitados() ,UsuarioSchema) 

class UsuarioResource(Resource): 
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if (datos):
            try:
                UsuarioService.modificarUsuario(datos)
                return {'Status':'Usuario modificado.'},200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': err.message},400
        return {'Error': 'Deben suministrarse los datos para modificar el usuario.'},400
       
    # @jwt_required()
    def post(self):
        datos = request.get_json()
        if (datos):
            try:
                UsuarioService.nuevoUsuario(datos)
                return {'Status':'Usuario creado.'},200
            except ValidationError as err:
                return {'error': err.messages},400
            except Exception as err:
                return {'error': err.message},400
        return {'Error': 'Deben suministrarse los datos para el alta de usuario.'},400
  
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

class Logins(Resource):

    def get(self):
        from app import app
        datos = request.get_json()
        if datos:
            usuario = UsuarioService.find_by_email(datos['email'])
            usuarioJson = CommonService.json(usuario,UsuarioSchema)
            if usuario:
                if check_password_hash(usuario.password, datos['password']):
                    token = jwt.encode(usuarioJson, app.config['SECRET_KEY'])
                    return jsonify({'token' : token.decode('UTF-8')})
                return {'Error': 'Las credenciales son incorrectas.'}, 400
            return {'Error': 'No existe ningún usuario con ese mail.'}, 400
    
    def post(self):
        datos = request.get_json()
        from app import app
        data = jwt.decode(datos['token'], app.config['SECRET_KEY'], algorithms=["HS256"])
        if not any(permiso['id_permiso'] <= 3 for permiso in data['permisos']):
            raise Exception(f"El usuario {data['email']}")
        return data, 200



