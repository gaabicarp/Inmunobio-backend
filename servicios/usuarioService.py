from models.mysql.usuario import Usuario
from schemas.usuarioSchema import UsuarioSchema, UsuarioSchemaModificar, UsuarioNuevoSchema
from exceptions.exception import ErrorPermisosJefeDeGrupo, ErrorJefeDeOtroGrupo, ErrorUsuarioInexistente, ErrorIntegranteDeOtroGrupo
from servicios.commonService import CommonService
from servicios.validationService import Validacion, ValidacionesUsuario
from werkzeug.security import generate_password_hash
from servicios.validationService import ValidacionesUsuario

class UsuarioService():
    @classmethod
    def modificarUsuario(cls, datos):
        from db import db
        UsuarioSchemaModificar().load(datos)
        usuario = UsuarioService.find_by_id(datos['id_usuario'])
        CommonService.updateAtributes(usuario, datos, 'permisos')
        cls.asignarPermisos(usuario, datos['permisos'])
        db.session.commit()

    @classmethod
    def asignarPermisos(cls, usuario, permisosDicts):
        '''recibe una lista con diccionarios de permisos y un usuario de la base
        si pudo encontrar los permisos en la base actualiza al usuario, sino devuelve
        mensaje de error.'''
        from servicios.permisosService import PermisosService
        usuario.permisos = PermisosService.permisosById(permisosDicts)

    @classmethod
    def nuevoUsuario(cls,datos):
            from db import db
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
            usuario = UsuarioNuevoSchema().load(datos)
            #cls.validarNuevoUsuario(usuario)
            #cls.agregarDatosUsuario(usuario,datos['permisos'])
            #db.session.add(usuario)
            #db.session.commit()

    @classmethod
    def agregarDatosUsuario(cls,usuario,permisos):
        cls.asignarPermisos(usuario,permisos)
        usuario.password = generate_password_hash(usuario.password, method='sha256')

    def validarNuevoUsuario(usuario):
        if len(usuario.password) < 8:
            raise Exception("La contraseña debe tener como mínimo 8 caracteres.")
        if Validacion.elMailEstaEnUso(usuario.email):
            raise Exception(f"Ya existe un/a usuario/a asociado/a con email {usuario.email}")

    @classmethod
    def find_by_email(cls, _email):
        resultado = Usuario.query.filter_by(email=_email, habilitado = True).first()
        if not resultado: raise ErrorUsuarioInexistente(_email)
        return resultado

    @classmethod
    def find_by_id(cls, _id):
        '''dada una id de usuario devuelve usuario si esta habilitado '''
        resultado = Usuario.query.filter_by(id=_id,habilitado=True).first()
        if not resultado: raise ErrorUsuarioInexistente(_id)
        return resultado

    @classmethod
    def findUsuariosHabilitados(cls):
        return Usuario.query.filter_by(habilitado=1).all()

    @classmethod
    def usuariosSinElPermiso(cls, id_permiso):
        from servicios.permisosService import  Permiso
        user = Usuario.query.filter(~Usuario.id_permisos.any(
            Permiso.id_permiso.in_([id_permiso])))
        if (user):
            return CommonService.jsonMany(user, UsuarioSchema)
        return user

    @classmethod
    def deshabilitarUsuario(cls, id_usuario):
        """recibe un usuario valido y modifica su estado habilitado a false"""
        # agregar schema de id usuario para verificar que se pase
        # -> oh por dios corregir esto hardcodeado  en algun momento
        from db import db
        CommonService.updateAtributes(
            UsuarioService.find_by_id(id_usuario), {'habilitado': False})
        db.session.commit()
        ValidacionesUsuario.desvincularDeProyectos(id_usuario)

    @classmethod
    def busquedaUsuariosID(cls, list_id_usuario):
        usuarios = []
        for id in list_id_usuario:
            usuario = UsuarioService.find_by_id(id)
            usuarios.append(usuario)
        return usuarios

    @classmethod
    def cambiarIdGrupo(cls, _id_usuario, idGrupo ):
        from db import db
        cls.find_by_id(_id_usuario).id_grupoDeTrabajo = idGrupo
        db.session.commit()
        
    @classmethod
    def asignarGrupoAJefe(cls, _id_usuario, idGrupo ):
        from db import db
        cls.find_by_id(_id_usuario).esJefeDe = idGrupo
        db.session.commit()

    @classmethod
    def validaAsignacionGrupo(cls, _id_usuario):
        usuario = cls.find_by_id(_id_usuario)
        if usuario.id_grupoDeTrabajo:
            raise ErrorIntegranteDeOtroGrupo(
                _id_usuario, usuario.id_grupoDeTrabajo)

    @classmethod
    def validarJefeDeGrupo(cls, _id_usuario,idNueva ):
        from servicios.permisosService import PermisosService
        jefe = cls.find_by_id(_id_usuario)
        if jefe.esJefeDe and jefe.esJefeDe != idNueva : raise ErrorJefeDeOtroGrupo(_id_usuario, jefe.esJefeDe)
        if not PermisosService.tieneElPermiso(jefe, PermisosService.jefeDeGrupo):
            raise ErrorPermisosJefeDeGrupo(_id_usuario)

