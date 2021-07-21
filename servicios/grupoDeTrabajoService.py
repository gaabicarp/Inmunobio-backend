from schemas.grupoTrabajoSchema import jefeDeGrupoSchema, ModificarGrupoDeTrabajoSchema, GrupoDeTrabajoSchema, GrupoDeTrabajo, NuevoGrupoDeTrabajoSchema
from servicios.usuarioService import UsuarioService
from exceptions.exception import ErrorGrupoInexistente, ErrorGrupoDeTrabajoGeneral
from servicios.commonService import CommonService


class GrupoDeTrabajoService():
    idGrupoDefault = 0

    def find_by_id(id):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()
        if(not grupo):
            raise ErrorGrupoInexistente()
        return grupo

    def find_by_nombre(_nombre):
        return GrupoDeTrabajo.objects(nombre=_nombre).first()

    @classmethod
    def modificarGrupo(cls, datos):
        grupoModificado = ModificarGrupoDeTrabajoSchema().load(datos)
        grupoAModificar = cls.find_by_id(grupoModificado.id_grupoDeTrabajo)
        cls.validarMiembros(cls.diferenciaConjuntos(grupoModificado.integrantes, grupoAModificar.integrantes))
        cls.validarJefe(grupoModificado.jefeDeGrupo,grupoModificado.id_grupoDeTrabajo)
        cls.modificacionMiembros(grupoModificado, grupoAModificar)
        grupoAModificar.update(integrantes= grupoModificado.integrantes, jefeDeGrupo= grupoModificado.jefeDeGrupo, nombre= grupoModificado.nombre)

    @classmethod
    def modificacionMiembros(cls, grupoNuevo, grupoViejo):
        cls.asignarIdGrupoMiembros(cls.diferenciaConjuntos(grupoNuevo.integrantes, grupoViejo.integrantes), grupoViejo.id_grupoDeTrabajo)
        cls.asignarIdGrupoMiembros(cls.diferenciaConjuntos(grupoViejo.integrantes, grupoNuevo.integrantes), cls.idGrupoDefault)
        if(grupoNuevo.jefeDeGrupo != grupoViejo.jefeDeGrupo):
            cls.nombrarJefe(grupoNuevo.jefeDeGrupo, grupoNuevo.id_grupoDeTrabajo)
            cls.desnombrarJefe(grupoViejo.jefeDeGrupo)

    @classmethod
    def diferenciaConjuntos(cls, primerConjunto, segundoConjunto):
        # Devuelve una lista de los items que estan en el primer conjunto y que no estan en el segundo.
        return [x for x in primerConjunto if x not in set(segundoConjunto)]

    @classmethod
    def nuevoGrupo(cls, datos):
        grupoCreado = NuevoGrupoDeTrabajoSchema().load(datos)
        cls.validarMiembros(grupoCreado.integrantes)
        cls.validarJefe(grupoCreado.jefeDeGrupo,cls.idGrupoDefault)
        grupoCreado.save()
        cls.asignarIDGrupo(grupoCreado, grupoCreado.id_grupoDeTrabajo)

    @classmethod
    def removerGrupo(cls, id_grupoDeTrabajo):
        grupoABorrar = cls.find_by_id(id_grupoDeTrabajo)
        cls.validarDelete(grupoABorrar)
        cls.asignarIDGrupo(grupoABorrar, cls.idGrupoDefault)
        grupoABorrar.delete()

    @classmethod
    def obtenerGrupoPorId(cls, idGrupoDeTrabajo):
        grupoConsulta = cls.find_by_id(idGrupoDeTrabajo)
        jefeDeGrupo = UsuarioService.find_by_id(grupoConsulta.jefeDeGrupo)
        return grupoConsulta, jefeDeGrupo.nombre

    @classmethod
    def asignarIDGrupo(cls, grupo, id):
        cls.asignarIdGrupoMiembros(grupo.integrantes, id)
        # UsuarioService.cambiarIdGrupo(grupo.jefeDeGrupo,id)
        # |-> ser jefe de grupo se asume como integrante, no hacefalta sumarlo a la lista de integrantes
        cls.nombrarJefe(grupo.jefeDeGrupo, id)

    @classmethod
    def asignarIdGrupoMiembros(cls, idIntegrantes, idGrupo):
        [UsuarioService.cambiarIdGrupo(id, idGrupo) for id in idIntegrantes]

    def obtenerTodosLosGrupos():
        return CommonService.jsonMany(GrupoDeTrabajo.objects.all(), GrupoDeTrabajoSchema)

    @classmethod
    def desnombrarJefe(cls, idJefe):
        UsuarioService.asignarGrupoAJefe(idJefe, cls.idGrupoDefault)

    @classmethod
    def nombrarJefe(cls, idJefe, idGrupo):
        UsuarioService.asignarGrupoAJefe(idJefe, idGrupo)

    def validarDelete(grupo):
        if grupo.grupoGral: raise ErrorGrupoDeTrabajoGeneral()

    @classmethod
    def validarMiembros(cls, integrantes):
        [UsuarioService.validaAsignacionGrupo(idIntegrante) for idIntegrante in integrantes]

    @classmethod
    def validarJefe(cls, id_jefeDeGrupo,idGrupo): UsuarioService.validarJefeDeGrupo(id_jefeDeGrupo,idGrupo)

    #este endpoint ya no se usa:
    @classmethod
    def modificarJefeGrupo(cls, datos):
        jefeDeGrupoSchema().load(datos)
        # TO-DO ver si esto se mover al schema
        grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
        cls.validarJefe(datos['jefeDeGrupo'],grupoAModificar.id_grupoDeTrabajo)
        cls.desnombrarJefe(grupoAModificar.jefeDeGrupo)
        cls.nombrarJefe(grupoAModificar.jefeDeGrupo,
                        grupoAModificar.id_grupoDeTrabajo)
        grupoAModificar.update(jefeDeGrupo=grupoAModificar.jefeDeGrupo)