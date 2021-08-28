from models.mongo.fuenteExperimental import FuenteExperimental
from schemas.fuenteExperimentalSchema import FuenteExperimentalSchema, FuenteExperimentalAnimalSchema, FuenteExperimentalOtroSchema
from models.mongo.grupoExperimental import GrupoExperimental
from dateutil import parser
from .validationService import Validacion
import datetime
from schemas.grupoExperimentalSchema import AgregarFuentesAlGrupoExperimentalSchema

class FuenteExperimentalService:

    @classmethod
    def find_by_id(cls, idFuenteExperimental):
        return FuenteExperimentalSchema().dump(FuenteExperimental.objects(id_fuenteExperimental = idFuenteExperimental, codigo__ne="").first())
    
    @classmethod
    def find_by_codigo(cls, codigoFuenteExperimental):
        return FuenteExperimentalSchema().dump(FuenteExperimental.objects(codigo = codigoFuenteExperimental).first())

    @classmethod
    def find_all_sin_asignar(cls):
        return FuenteExperimentalSchema().dump(FuenteExperimental.objects(tipo="Animal", grupoExperimental="", codigo__ne="").all(), many=True)
    
    #Consultar qué datos se piden cuando se carga el animal y cuáles cuando se crea una nueva fuente experimental
    @classmethod
    def nuevasFuentesExperimentales(cls, datos):
        grupoExperimental = AgregarFuentesAlGrupoExperimentalSchema().load(datos)
        fuentesExperimentales = list(map(lambda fuente: FuenteExperimentalAnimalSchema().load(fuente) if fuente['tipo'] == "Animal" else FuenteExperimentalOtroSchema().load(fuente), datos['fuentesExperimentales']))
        grupoExperimental.fuentesExperimentales = fuentesExperimentales
        cls.validarGrupoExperimental(grupoExperimental)
        if fuentesExperimentales[0].tipo == "Animal":
            cls.validarAnimales(cls, grupoExperimental)
            cls.nuevasFuentesAnimales(grupoExperimental)
        else:
            cls.nuevasFuentesOtros(fuentesExperimentales)
        cls.actualizarFuentesExperimentalesEnGrupoExperimental(grupoExperimental)
        return {"Status" : "Se crearon las fuentes experimentales",}, 200
    
    def nuevasFuentesAnimales(grupoExperimental):
        for fuente in grupoExperimental.fuentesExperimentales:
           FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(
                    codigo = fuente.codigo,
                    codigoGrupoExperimental = fuente.codigoGrupoExperimental
                )

    def nuevasFuentesOtros(fuentesExperimentales):
        for fuente in fuentesExperimentales:
            fuente.idJaula = 0
            fuente.save()

    def actualizarFuentesExperimentalesEnGrupoExperimental(grupoExperimental):
        fuentesExperimentales =  FuenteExperimental.objects(codigoGrupoExperimental = grupoExperimental.codigo).all()
        fuentesExperimentalesDic = FuenteExperimentalSchema(exclude=['id_jaula', 'baja', 'id_proyecto']).dump(fuentesExperimentales, many=True)
        GrupoExperimental.objects(id_grupoExperimental = grupoExperimental.id_grupoExperimental).update(
            fuentesExperimentales = fuentesExperimentalesDic
        )
    @classmethod
    def validarGrupoExperimental(cls, grupoExperimental):
        if not Validacion.existeElgrupoExperimental(grupoExperimental):
            raise Exception("El grupo experimental debe existir y estar habilitado")
        if not Validacion.elExperimentoEstaFinalizado(grupoExperimental.id_experimento):
            raise Exception("El experimento debe estar activo.")
        if not Validacion.elGrupoExperimentalEsDelMismoTipoQueLasFuentes(grupoExperimental):
            raise Exception("El grupo experimental y las fuentes tienen que ser del mismo tipo")
        if not Validacion.todasLasFuentesTienenElMismoGrupoExperimental(grupoExperimental):
            raise Exception("El -codigoGrupoExperimental-de todas las fuentes experimentales deben ser mismo -código- del grupo experimental.")
    
    def validarAnimales(self, grupoExperimental):
        if not Validacion.losAnimalesEstanHabilitados(grupoExperimental.fuentesExperimentales):
            raise Exception("Los animales deben existir y no pueden estar en estado de baja.")
        if not Validacion.losAnimalesNoTienenGrupoExperimental(grupoExperimental.fuentesExperimentales):
            raise Exception("Los animales ya están en uso.")
        if not Validacion.losAnimalesPertenecenAlMismoProyectoDelExperimento(grupoExperimental):
            raise Exception("Los animales deben pertenecer al mismo proyecto.")



