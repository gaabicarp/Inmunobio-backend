from db import db
from models.mysql.usuario import Usuario
from schemas.usuarioSchema import UsuarioSchema,UsuarioSchemaModificar,UsuarioNuevoSchema,usuarioIDSchema
from marshmallow import Schema, ValidationError
from servicios.permisosService import PermisosService,Permiso
from exceptions.exception import ErrorPermisoInexistente,ErrorUsuarioInexistente,ErrorUsuariosInexistentes
from servicios.commonService import CommonService
class UsuarioService():

    @classmethod
    def modificarUsuario(cls,datos):        
        try:
            UsuarioSchemaModificar().load(datos) 
            usuario = UsuarioService.find_by_id(datos['id_usuario'])
            CommonService.updateAtributes(usuario,datos,'permisos')
            db.session.commit()
            cls.asignarPermisos(usuario,datos['permisos'])
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'Error': err.messages}, 400
        except (ErrorUsuarioInexistente,ErrorPermisoInexistente) as err:
            return {'Error': err.message},400

    @classmethod
    def asignarPermisos(cls,usuario,permisosDicts):
        '''recibe una lista con diccionarios de permisos y un usuario de la base
        si pudo encontrar los permisos en la base actualiza al usuario, sino devuelve
        mensaje de error.'''
        permisosObject = PermisosService.permisosById(permisosDicts)
        usuario.setPermiso(permisosObject)
        db.session.add(usuario)
        db.session.commit()
  

    @classmethod
    def nuevoUsuario(cls,datos):
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
        try:
            usuario = UsuarioNuevoSchema().load(datos) 
            return cls.asignarPermisos(usuario,datos['permisos'])
        except ValidationError as err:
            return {'error': err.messages},400

    @classmethod
    def find_by_email(cls, _email):
        return Usuario.query.filter_by(email=_email).first()

    @classmethod
    def find_by_id(cls, _id):
        '''dada una id de usuario devuelve usuario si esta habilitado '''
        resultado = Usuario.query.filter_by(id_usuario=_id,habilitado=True).first()
        if not resultado: raise ErrorUsuarioInexistente(_id)
        return resultado
        
    @classmethod
    def findUsuariosHabilitados(cls):
        resultado = Usuario.query.filter_by(habilitado=1).all()
        if not resultado : raise ErrorUsuariosInexistentes()
        return CommonService.jsonMany(resultado,UsuarioSchema) 
    
    @classmethod
    def usuariosSinElPermiso(cls,id_permiso):
        user = Usuario.query.filter(~Usuario.id_permisos.any(Permiso.id_permiso.in_([id_permiso])))
        if (user):
            return CommonService.jsonMany(user,UsuarioSchema)
        return user



    @classmethod
    def deshabilitarUsuario(cls,datos):
        """recibe un usuario valido y modifica su estado habilitado a false"""
        #agregar schema de id usuario para verificar que se pase
        try:
            usuarioIDSchema().load(datos)
            usuario = UsuarioService.find_by_id(datos['id_usuario'])
            CommonService.updateAtributes(usuario,{'habilitado': False}) # -> oh por dios corregir esto hardcodeado esto en algun momento 
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorUsuarioInexistente as err:
            return {'Error':err.message},400

    @classmethod
    def busquedaUsuario(cls,_id_usuario):
        try:
            usuario = UsuarioService.find_by_id(_id_usuario)
            return CommonService.json(usuario,UsuarioSchema)
        except ErrorUsuarioInexistente as err:
            return {'Error': err.message},400