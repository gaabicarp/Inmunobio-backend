from db import db 
from models.mysql.usuario import Usuario
from schemas.usuarioSchema import UsuarioSchema,UsuarioSchemaModificar,UsuarioNuevoSchema
from servicios.permisosService import PermisosService,Permiso
from exceptions.exception import ErrorUsuarioExistente,ErrorUsuarioInexistente
from servicios.commonService import CommonService
from servicios.validationService import ValidacionesUsuario

class UsuarioService():
    @classmethod
    def modificarUsuario(cls,datos):        
            UsuarioSchemaModificar().load(datos) 
            usuario = UsuarioService.find_by_id(datos['id_usuario'])
            CommonService.updateAtributes(usuario,datos,'permisos')
            cls.asignarPermisos(usuario,datos['permisos'])
            db.session.commit()
   

    @classmethod
    def asignarPermisos(cls,usuario,permisosDicts):
        '''recibe una lista con diccionarios de permisos y un usuario de la base
        si pudo encontrar los permisos en la base actualiza al usuario, sino devuelve
        mensaje de error.'''
        #PermisosService.validarPermisos(permisosDicts)
        usuario.permisos = PermisosService.permisosById(permisosDicts)

    @classmethod
    def nuevoUsuario(cls,datos):
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
            usuario = UsuarioNuevoSchema().load(datos) 
            cls.validarUsuarioExistente(usuario)
            cls.asignarPermisos(usuario,datos['permisos'])
            db.session.add(usuario)
            db.session.commit()
 
    @classmethod
    def validarUsuarioExistente(cls,usuario):
        if (cls.find_by_email(usuario.email)): raise ErrorUsuarioExistente(usuario.email)

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
        return Usuario.query.filter_by(habilitado=1).all()
        
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
        CommonService.updateAtributes(UsuarioService.find_by_id(id_usuario),{'habilitado': False}) # -> oh por dios corregir esto hardcodeado  en algun momento 
        db.session.commit()
        ValidacionesUsuario.desvincularDeProyectos(id_usuario)

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



