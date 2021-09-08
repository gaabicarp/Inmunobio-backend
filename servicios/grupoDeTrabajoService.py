from schemas.grupoTrabajoSchema import jefeDeGrupoSchema, ModificarGrupoDeTrabajoSchema, GrupoDeTrabajoSchema, GrupoDeTrabajo, NuevoGrupoDeTrabajoSchema
from servicios.commonService import CommonService


class GrupoDeTrabajoService():

    idGrupoDefault = 0

    def find_by_id(id):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=id).first()
        if(not grupo):
            raise Exception("Grupo de trabajo inexistente.")
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
            cls.nombrarJefe(grupoViejo.jefeDeGrupo, cls.idGrupoDefault)

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
        cls.agregarDatosGrupo(grupoConsulta)
        return grupoConsulta

    @classmethod
    def agregarDatosGrupo(cls,grupo):
        from servicios.usuarioService import UsuarioService
        grupo.jefeDeGrupo = UsuarioService.find_by_id(grupo.jefeDeGrupo)
        grupo.integrantes = UsuarioService.busquedaUsuariosID(grupo.integrantes)

    @classmethod
    def asignarIDGrupo(cls, grupo, id):
        cls.asignarIdGrupoMiembros(grupo.integrantes, id)
        # UsuarioService.cambiarIdGrupo(grupo.jefeDeGrupo,id)
        # |-> ser jefe de grupo se asume como integrante, no hacefalta sumarlo a la lista de integrantes
        cls.nombrarJefe(grupo.jefeDeGrupo, id)

    @classmethod
    def asignarIdGrupoMiembros(cls, idIntegrantes, idGrupo):
        from servicios.usuarioService import UsuarioService
        [UsuarioService.cambiarIdGrupo(id, idGrupo) for id in idIntegrantes]

    def obtenerTodosLosGrupos():
        return CommonService.jsonMany(GrupoDeTrabajo.objects.all(), GrupoDeTrabajoSchema)

    @classmethod
    def nombrarJefe(cls, idJefe, idGrupo):
        from servicios.usuarioService import UsuarioService
        UsuarioService.asignarGrupoAJefe(idJefe, idGrupo)

    def validarDelete(grupo):
        if grupo.grupoGral: raise Exception("El grupo es general y no puede darse de baja." )

    @classmethod
    def validarMiembros(cls, integrantes):
        from servicios.usuarioService import UsuarioService
        [UsuarioService.validaAsignacionGrupo(idIntegrante) for idIntegrante in integrantes]

    @classmethod
    def validarJefe(cls, id_jefeDeGrupo,idGrupo): 
        from servicios.usuarioService import UsuarioService
        UsuarioService.validarJefeDeGrupo(id_jefeDeGrupo,idGrupo)

    #-------------------este endpoint ya no se usa:
    @classmethod
    def modificarJefeGrupo(cls, datos):
        jefeDeGrupoSchema().load(datos)
        grupoAModificar = cls.find_by_id(datos['id_grupoDeTrabajo'])
        cls.validarJefe(datos['jefeDeGrupo'],grupoAModificar.id_grupoDeTrabajo)
        cls.desnombrarJefe(grupoAModificar.jefeDeGrupo)
        cls.nombrarJefe(grupoAModificar.jefeDeGrupo,
                        grupoAModificar.id_grupoDeTrabajo)
        grupoAModificar.update(jefeDeGrupo=grupoAModificar.jefeDeGrupo)