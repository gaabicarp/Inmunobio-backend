from schemas.grupoTrabajoSchema import jefeDeGrupoSchema,ModificarGrupoDeTrabajoSchema,GrupoDeTrabajoSchema,GrupoDeTrabajo,NuevoGrupoDeTrabajoSchema,GrupoDeTrabajoIDSchema
from marshmallow import  ValidationError
from servicios.usuarioService import UsuarioService
from exceptions.exception import ErrorGrupoInexistente,ErrorUsuarioInexistente,ErrorGrupoDeTrabajoGeneral
from servicios.commonService import CommonService

class GrupoDeTrabajoService():
    def find_by_id(id):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()
        if(not grupo):
            raise ErrorGrupoInexistente()
        return grupo

    def find_by_nombre(_nombre):
        return GrupoDeTrabajo.objects(nombre = _nombre).first()

    @classmethod
    def modificarMiembrosGrupo(cls,datos):
            ModificarGrupoDeTrabajoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            cls.validarMiembros(datos['integrantes']+[datos['jefeDeGrupo']])
            grupoAModificar.update(integrantes=datos['integrantes'],
            jefeDeGrupo=datos['jefeDeGrupo'],nombre= datos['nombre']
            )
            
    @classmethod
    def nuevoGrupo(cls,datos):
            grupoCreado = NuevoGrupoDeTrabajoSchema().load(datos)
            cls.validarMiembros([grupoCreado.jefeDeGrupo]+datos['integrantes'])
            #falta ver si tiene permisos nivel 4 
            grupoCreado.save()
            cls.asignarIDGrupo(grupoCreado)

    @classmethod
    def removerGrupo(cls,id_grupoDeTrabajo):
            grupoABorrar = GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)
            cls.validarDelete(grupoABorrar)
            grupoABorrar.delete()

    def obtenerGrupoPorId(idGrupoDeTrabajo):
        grupoConsulta= GrupoDeTrabajoService.find_by_id(idGrupoDeTrabajo)
        jefeDeGrupo = UsuarioService.find_by_id(grupoConsulta.jefeDeGrupo)
        return grupoConsulta,jefeDeGrupo.nombre

    def validarDelete(grupo):
        if grupo.grupoGral:
            raise ErrorGrupoDeTrabajoGeneral()

    def validarMiembros(integrantes):
        for idIntegrante in integrantes:
            UsuarioService.find_by_id(idIntegrante)

    def asignarIDGrupo(grupo):
        for idIntegrante in grupo.integrantes:
            UsuarioService.cambiarIdGrupo(idIntegrante,grupo.id_grupoDeTrabajo)
        UsuarioService.cambiarIdGrupo(grupo.jefeDeGrupo,grupo.id_grupoDeTrabajo)
        UsuarioService.asignarGrupo(grupo.jefeDeGrupo,grupo.id_grupoDeTrabajo)

    def obtenerTodosLosGrupos():
        return CommonService.jsonMany(GrupoDeTrabajo.objects.all(),GrupoDeTrabajoSchema)
    
    @classmethod
    def modificarJefeGrupo(cls,datos):
            jefeDeGrupoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            cls.validarMiembros([datos['jefeDeGrupo']])
            grupoAModificar.update(jefeDeGrupo=datos['jefeDeGrupo'])
            cls.asignarIDGrupo(grupoAModificar)
  