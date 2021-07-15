from schemas.grupoTrabajoSchema import jefeDeGrupoSchema,ModificarGrupoDeTrabajoSchema,GrupoDeTrabajoSchema,GrupoDeTrabajo,NuevoGrupoDeTrabajoSchema,GrupoDeTrabajoIDSchema
from servicios.usuarioService import UsuarioService
from exceptions.exception import ErrorGrupoInexistente,ErrorGrupoDeTrabajoGeneral
from servicios.commonService import CommonService

class GrupoDeTrabajoService():
    def find_by_id(id):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()
        if(not grupo): raise ErrorGrupoInexistente()
        return grupo

    def find_by_nombre(_nombre):
        return GrupoDeTrabajo.objects(nombre = _nombre).first()

    @classmethod
    def modificarMiembrosGrupo(cls,datos):
            ModificarGrupoDeTrabajoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            cls.validarMiembros(datos['integrantes'],datos['jefeDeGrupo'])
            grupoAModificar.update(integrantes=datos['integrantes'],
            jefeDeGrupo=datos['jefeDeGrupo'],nombre= datos['nombre']
            )
            
    @classmethod
    def nuevoGrupo(cls,datos):
            grupoCreado = NuevoGrupoDeTrabajoSchema().load(datos)
            print(grupoCreado.integrantes)
            cls.validarMiembros(grupoCreado.integrantes)
            cls.validarJefe(grupoCreado.jefeDeGrupo)
            grupoCreado.save()
            cls.asignarIDGrupo(grupoCreado,grupoCreado.id_grupoDeTrabajo)

    @classmethod
    def removerGrupo(cls,id_grupoDeTrabajo):
            grupoABorrar = GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)
            cls.validarDelete(grupoABorrar)
            cls.asignarIDGrupo(grupoABorrar,0)
            grupoABorrar.delete()

    def obtenerGrupoPorId(idGrupoDeTrabajo):
        grupoConsulta= GrupoDeTrabajoService.find_by_id(idGrupoDeTrabajo)
        jefeDeGrupo = UsuarioService.find_by_id(grupoConsulta.jefeDeGrupo)
        return grupoConsulta,jefeDeGrupo.nombre

    def validarDelete(grupo):
        if grupo.grupoGral: raise ErrorGrupoDeTrabajoGeneral()

    @classmethod
    def validarMiembros(cls,integrantes):
        [UsuarioService.validaAsignacionGrupo(idIntegrante) for idIntegrante in integrantes]

    @classmethod
    def validarJefe(cls, id_jefeDeGrupo):
        UsuarioService.validarJefeDeGrupo(id_jefeDeGrupo)

    def asignarIDGrupo(grupo,id):
        for idIntegrante in grupo.integrantes:
            UsuarioService.cambiarIdGrupo(idIntegrante,id)
        UsuarioService.cambiarIdGrupo(grupo.jefeDeGrupo,id)
        UsuarioService.asignarGrupoAJefe(grupo.jefeDeGrupo,id)

    def obtenerTodosLosGrupos():
        return CommonService.jsonMany(GrupoDeTrabajo.objects.all(),GrupoDeTrabajoSchema)
    
    @classmethod
    def modificarJefeGrupo(cls,datos):
            jefeDeGrupoSchema().load(datos)
            grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
            cls.validarMiembros([datos['jefeDeGrupo']])
            grupoAModificar.update(jefeDeGrupo=datos['jefeDeGrupo'])
            #TO-DO ver la asignacion esta de miembros
            cls.asignarIDGrupo(grupoAModificar)
  