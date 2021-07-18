from db import db 
from models.mysql.usuario import Usuario
from schemas.usuarioSchema import UsuarioSchema,UsuarioSchemaModificar,UsuarioNuevoSchema,usuarioIDSchema
from marshmallow import ValidationError
from servicios.permisosService import PermisosService,Permiso
from exceptions.exception import ErrorPermisoInexistente,ErrorUsuarioInexistente,ErrorUsuariosInexistentes
from servicios.commonService import CommonService
from servicios.validationService import Validacion, ValidacionesUsuario
from werkzeug.security import generate_password_hash
class UsuarioService():

    @classmethod
    def modificarUsuario(cls,datos):        
        try:
            UsuarioSchemaModificar().load(datos) 
            usuario = UsuarioService.find_by_id(datos['id_usuario'])
            CommonService.updateAtributes(usuario,datos,'permisos')
            cls.asignarPermisos(usuario,datos['permisos'])
            db.session.commit()
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

    @classmethod
    def nuevoUsuario(cls,datos):
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
        try:
            usuario = UsuarioNuevoSchema().load(datos)
            cls.validarNuevoUsuario(usuario)
            cls.asignarPermisos(usuario,datos['permisos'])
            hashed_password = generate_password_hash(usuario.password, method='sha256')
            usuario.password = hashed_password
            db.session.add(usuario)
            db.session.commit()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorPermisoInexistente as err:
            return {'error': err.message},400
        except Exception as err:
            return {'error': str(err)}, 400
    
    def validarNuevoUsuario(usuario):
        if len(usuario.password) < 8:
            raise Exception("La contraseña debe tener como mínimo 8 caracteres.")
        if Validacion.elMailEstaEnUso(usuario.email):
            raise Exception("El email ya se encuentra en uso.")

    @classmethod
    def find_by_email(cls, _email):
        usuario = Usuario.query.filter_by(email=_email).first()
        return usuario

    @classmethod
    def find_by_id(cls, _id):
        '''dada una id de usuario devuelve usuario si esta habilitado '''
        resultado = Usuario.query.filter_by(id=_id,habilitado=True).first()
        if not resultado: raise ErrorUsuarioInexistente(_id)
        return resultado
        
    @classmethod
    def findUsuariosHabilitados(cls):
        resultado = Usuario.query.filter_by(habilitado=1).all()
        return CommonService.jsonMany(resultado,UsuarioSchema) 
    
    @classmethod
    def usuariosSinElPermiso(cls,id_permiso):
        user = Usuario.query.filter(~Usuario.id_permisos.any(Permiso.id_permiso.in_([id_permiso])))
        if (user):
            return CommonService.jsonMany(user,UsuarioSchema)
        return user

    @classmethod
    def deshabilitarUsuario(cls,id_usuario):
        """recibe un usuario valido y modifica su estado habilitado a false"""
        #agregar schema de id usuario para verificar que se pase
        try:
            CommonService.updateAtributes(UsuarioService.find_by_id(id_usuario),{'habilitado': False}) # -> oh por dios corregir esto hardcodeado  en algun momento 
            db.session.commit()
            ValidacionesUsuario.desvincularDeProyectos(id_usuario)
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
    
    @classmethod
    def busquedaUsuariosID(cls,list_id_usuario):
        usuarios = []
        for id in list_id_usuario:
            usuario = UsuarioService.find_by_id(id)
            usuarios.append(usuario)
        return usuarios

    @classmethod
    def cambiarIdGrupo(cls,_id_usuario, idGrupo):
        UsuarioService.find_by_id(_id_usuario).id_grupoDeTrabajo = idGrupo
        db.session.commit()
        
    @classmethod
    def asignarGrupo(cls,_id_usuario, idGrupo):
        UsuarioService.find_by_id(_id_usuario).esJefeDe = idGrupo
        db.session.commit()



