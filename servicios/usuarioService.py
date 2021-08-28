from models.mysql.usuario import Usuario
from schemas.usuarioSchema import UsuarioSchemaModificar, UsuarioNuevoSchema
from servicios.commonService import CommonService
from servicios.validationService import  ValidacionesUsuario
from werkzeug.security import generate_password_hash,check_password_hash

class UsuarioService():
    @classmethod
    def modificarUsuario(cls, datos):
        usuario = cls.validarModificacion(datos)
        CommonService.updateAtributes(usuario , datos, ['permisos','password'])
        cls.modificacionPassword(usuario,datos['password'])
        cls.asignarPermisos(usuario, datos['permisos'])

        from db import db
        db.session.commit()

    @classmethod
    def validarModificacion(cls, datos):
        UsuarioSchemaModificar().load(datos)
        usuarioAnt = UsuarioService.find_by_id(datos['id'])
        cls.validaModificacionEmail(usuarioAnt,datos['email'])
        return usuarioAnt

    @classmethod
    def asignarPermisos(cls, usuario, permisosDicts):
        from servicios.permisosService import PermisosService
        usuario.permisos = PermisosService.permisosById(permisosDicts)

    @classmethod
    def nuevoUsuario(cls,datos):
        usuario = UsuarioNuevoSchema().load(datos)
        cls.validarEmail(usuario.email)
        cls.hashPassword(usuario,usuario.password)
        from db import db
        db.session.add(usuario)
        db.session.commit()

    @classmethod
    def hashPassword(cls,usuario,password):
        usuario.password = generate_password_hash(password, method='sha256')
         
    @classmethod
    def validaModificacionEmail(cls,usuario,email):
        if usuario.email != email : cls.validarEmail(email)

    @classmethod
    def modificacionPassword(cls,usuario,password):
        if not check_password_hash(usuario.password, password): cls.hashPassword(usuario,password)

    @classmethod
    def validarEmail(cls,email ):
        if cls.find_by_email(email):
            raise Exception(f"Ya existe un/a usuario/a asociado/a con el email indicado.") 

    @classmethod
    def find_by_email(cls, _email):
        return Usuario.query.filter_by(email=_email, habilitado = True).first()

    @classmethod
    def find_by_id(cls, _id):
        '''dada una id de usuario devuelve usuario si esta habilitado '''
        resultado = Usuario.query.filter_by(id=_id,habilitado=True).first()
        if not resultado: raise Exception(f"No hay usuario/a asociado/a con id {_id}")
        return resultado

    @classmethod
    def findUsuariosHabilitados(cls):
        return Usuario.query.filter_by(habilitado=True).all()

    @classmethod
    def usuariosSinElPermiso(cls, id_permiso):
        from models.mysql.permiso import Permiso
        return Usuario.query.filter(~Usuario.permisos.any(
            Permiso.id_permiso.in_([id_permiso])))            

    @classmethod
    def deshabilitarUsuario(cls, id_usuario):
        from db import db
        usuario = UsuarioService.find_by_id(id_usuario)
        ValidacionesUsuario.jefeDeProyecto(usuario)  
        usuario.habilitado =False 
        db.session.commit()
        ValidacionesUsuario.desvincularDeProyectos(id_usuario)

    @classmethod
    def busquedaUsuariosID(cls, list_id_usuario):
        return list(map(UsuarioService.find_by_id,list_id_usuario))

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
            raise Exception(f"El usuario con id {_id_usuario}",
            " ya se encuentra asignado al grupo de trabajo con id.{usuario.id_grupoDeTrabajo}")

    @classmethod
    def validarJefeDeGrupo(cls, _id_usuario,idNueva ):
        from servicios.permisosService import PermisosService
        jefe = cls.find_by_id(_id_usuario)
        if jefe.esJefeDe and jefe.esJefeDe != idNueva : raise Exception(f"El usuario con id {_id_usuario} ya es jefe del grupo {jefe.esJefeDe}")
        if not PermisosService.tieneElPermiso(jefe, PermisosService.jefeDeGrupo):
            raise Exception(f"El usuario con id {_id_usuario} no posee permisos para ser jefe de grupo.")
    
        