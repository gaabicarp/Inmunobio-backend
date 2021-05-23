from schemas.grupoTrabajoSchema import jefeDeGrupoSchema,ModificarGrupoDeTrabajoSchema,GrupoDeTrabajoSchema,GrupoDeTrabajo,NuevoGrupoDeTrabajoSchema,GrupoDeTrabajoIDSchema
from marshmallow import  ValidationError
from servicios.usuarioService import UsuarioService
from exceptions.exception import ErrorGrupoInexistente,ErrorUsuarioInexistente
from servicios.commonService import CommonService

class GrupoDeTrabajoService:
    def find_by_id(id):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()
        if(not grupo):
            raise ErrorGrupoInexistente()
        return grupo

    def find_by_nombre(_nombre):
        return GrupoDeTrabajo.objects(nombre = _nombre).first()

    @classmethod
    def modificarMiembrosGrupo(cls,datos):
        try:
            ModificarGrupoDeTrabajoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            cls.validarMiembros(datos['integrantes']+[datos['jefeDeGrupo']])
            grupoAModificar.update(integrantes=datos['integrantes'],
            jefeDeGrupo=datos['jefeDeGrupo'],nombre= datos['nombre']
            )
            return {'Status':'ok'},200  
        except ValidationError as err:
            return {'error': err.messages},400
        except (ErrorGrupoInexistente,ErrorUsuarioInexistente) as err:
            return {'Error':err.message},400

    @classmethod
    def modificarJefeGrupo(cls,datos):
        try:
            jefeDeGrupoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            cls.validarMiembros([datos['jefeDeGrupo']])
            grupoAModificar.update(jefeDeGrupo=datos['jefeDeGrupo'])
            cls.asignarIDGrupo(grupoAModificar)
            return {'Status':'ok'},200  
        except ValidationError as err:
            return {'error': err.messages},400
        except (ErrorGrupoInexistente,ErrorUsuarioInexistente) as err:
            return {'Error':err.message},400
            
    @classmethod
    def nuevoGrupo(cls,datos):
        try:
            grupoCreado = NuevoGrupoDeTrabajoSchema().load(datos)
            cls.validarMiembros([grupoCreado.jefeDeGrupo]+datos['integrantes'])
            #falta ver si tiene permisos nivel 4 
            grupoCreado.save()
            cls.asignarIDGrupo(grupoCreado)
            return {'Status':'ok'},200  
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorUsuarioInexistente as err:
            return {'Error': err.message},400

    @classmethod
    def removerGrupo(cls,datos):
        try:
            GrupoDeTrabajoIDSchema().load(datos)
            grupoABorrar = GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo'])
            if(cls.validarDelete(grupoABorrar)):
                grupoABorrar.delete()
                return {'Status':'ok'},200
            return {'Status': 'El grupo no puede ser dado de baja por ser grupo general'},400
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400

    def obtenerGrupoPorId(idGrupoDeTrabajo):
        try:
            grupoConsulta= GrupoDeTrabajoService.find_by_id(idGrupoDeTrabajo)
            jefeDeGrupo = UsuarioService.find_by_id()
            return CommonService.json(grupoConsulta,GrupoDeTrabajoSchema),jefeDeGrupo.nombre
        except (ErrorGrupoInexistente,ErrorUsuarioInexistente) as err:
            return {'Error':err.message},400

    def validarDelete(grupo):
        return not grupo.grupoGral

    def validarMiembros(integrantes):
        '''recibe una listacon id de usuarios devuelve true si todos existen o false en caso contrario'''
        for idIntegrante in integrantes:
            UsuarioService.find_by_id(idIntegrante)

    def asignarIDGrupo(grupo):
        for idIntegrante in grupo.integrantes:
            UsuarioService.cambiarIdGrupo(idIntegrante,grupo.id_grupoDeTrabajo)
        UsuarioService.cambiarIdGrupo(grupo.jefeDeGrupo,grupo.id_grupoDeTrabajo)
        UsuarioService.asignarGrupo(grupo.jefeDeGrupo,grupo.id_grupoDeTrabajo)

    def obtenerTodosLosGrupos():
        return CommonService.jsonMany(GrupoDeTrabajo.objects.all(),GrupoDeTrabajoSchema)