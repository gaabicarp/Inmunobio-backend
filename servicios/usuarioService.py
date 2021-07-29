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
        UsuarioSchemaModificar().dump(datos)
        usuario = UsuarioService.find_by_id(datos['id'])
        cls.validarEmail(usuario.email,datos['email'])
        CommonService.updateAtributes(usuario, datos, 'permisos')
        cls.hashPassword(usuario)
        cls.asignarPermisos(usuario, datos['permisos'])
        db.session.commit()

    @classmethod
    def asignarPermisos(cls, usuario, permisosDicts):
        from servicios.permisosService import PermisosService
        usuario.permisos = PermisosService.permisosById(permisosDicts)

    @classmethod
    def nuevoUsuario(cls,datos):
            from db import db
        #minimo un permiso  el 5, aun no esta validado , solo valida que sean permisos que existen
            usuario = UsuarioNuevoSchema().load(datos)
            cls.validarEmail(usuario.email)
            cls.hashPassword(usuario)
            db.session.add(usuario)
            db.session.commit()

    @classmethod
    def hashPassword(cls,usuario):
        cls.validarPassword(usuario.password)
        usuario.password = generate_password_hash(usuario.password, method='sha256')

    @classmethod
    def validarEmail(cls,email, emailAnt = None):
        if cls.find_by_email(email) and (email != emailAnt):
            raise Exception(f"Ya existe un/a usuario/a asociado/a con el email indicado.") 

    @classmethod
    def validarPassword(cls,password):
        if len(password) < 8:
                raise Exception("La contraseña debe tener como mínimo 8 caracteres.")
    @classmethod
    def find_by_email(cls, _email):
        from db import db
        return Usuario.query.filter_by(email=_email, habilitado = True).first()
        #if not resultado: raise ErrorUsuarioInexistente(_email)
        #return resultado , hay que sacar el error xq se usa en la aut. 

    @classmethod
    def find_by_id(cls, _id):
        '''dada una id de usuario devuelve usuario si esta habilitado '''
        resultado = Usuario.query.filter_by(id=_id,habilitado=True).first()
        if not resultado: raise ErrorUsuarioInexistente(_id)
        return resultado

    @classmethod
    def findUsuariosHabilitados(cls):
        return Usuario.query.filter_by(habilitado=True).all()

    @classmethod
    def usuariosSinElPermiso(cls, id_permiso):
        return Usuario.query.filter(~Usuario.permisos.any(
            Permiso.id_permiso.in_([id_permiso])))            


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

