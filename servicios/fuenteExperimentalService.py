from models.mongo.fuenteExperimental import FuenteExperimental
from schemas.fuenteExperimentalSchema import FuenteExperimentalAnimalBSchema,FuenteExperimentalSchema, FuenteExperimentalAnimalSchema, FuenteExperimentalOtroSchema
from models.mongo.grupoExperimental import GrupoExperimental
from dateutil import parser
from .validationService import Validacion
from schemas.grupoExperimentalSchema import AgregarFuentesAlGrupoExperimentalSchema

class FuenteExperimentalService:
    @classmethod
    def find_by_id(cls, idFuenteExperimental):
        fuente =  FuenteExperimental.objects(id_fuenteExperimental = idFuenteExperimental, codigo__ne="").first()
        if not fuente : raise Exception( f"No se encontró una fuente experimental para el id {idFuenteExperimental}")
        return fuente

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
        fuentesExperimentales = list(map(lambda fuente: FuenteExperimentalAnimalBSchema().load(fuente) if fuente['tipo'] == "Animal" else FuenteExperimentalOtroSchema().load(fuente), datos['fuentesExperimentales']))        
        cls.agregarCodigoAFuentes(fuentesExperimentales,grupoExperimental)
        grupoExperimental.fuentesExperimentales = fuentesExperimentales
        cls.validarGrupoExperimental(grupoExperimental)
        if fuentesExperimentales[0].tipo == "Animal":
            cls.validarAnimales(grupoExperimental)
            cls.nuevasFuentesAnimales(grupoExperimental)
        else:
            cls.nuevasFuentesOtros(grupoExperimental,fuentesExperimentales)
        cls.actualizarFuentesExperimentalesEnGrupoExperimental(grupoExperimental) 


    @classmethod
    def agregarCodigoAFuentes(cls,fuentesExperimentales,grupoExperimental):
        [ cls.asignarCodigo(fuente,grupoExperimental.codigo) for fuente in fuentesExperimentales]

    @classmethod
    def asignarCodigo(cls,fuente,codigoGrupo):
        fuente.codigoGrupoExperimental = codigoGrupo

    def nuevasFuentesAnimales(grupoExperimental):
        for fuente in grupoExperimental.fuentesExperimentales:
           FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(
                    codigo = fuente.codigo,
                    codigoGrupoExperimental = fuente.codigoGrupoExperimental) 

    @classmethod
    def nuevasFuentesOtros(cls,grupoExperimental,fuentesExperimentales):
        for fuente in fuentesExperimentales:
            fuente.idJaula = 0
            fuente.save()

    def actualizarFuentesExperimentalesEnGrupoExperimental(grupoExperimental):
        fuentesExperimentalesDic = FuenteExperimentalSchema().dump(grupoExperimental.fuentesExperimentales, many=True) 
        GrupoExperimental.objects(id_grupoExperimental = grupoExperimental.id_grupoExperimental).update_one(push_all__fuentesExperimentales = fuentesExperimentalesDic)
        
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
    
    @classmethod
    def validarAnimales(cls, grupoExperimental):
        if not Validacion.losAnimalesEstanHabilitados(grupoExperimental.fuentesExperimentales):
            raise Exception("Los animales deben existir y no pueden estar en estado de baja.")
        if not Validacion.losAnimalesNoTienenGrupoExperimental(grupoExperimental.fuentesExperimentales):
            raise Exception("Los animales ya están en uso.")
        if not Validacion.losAnimalesPertenecenAlMismoProyectoDelExperimento(grupoExperimental):
            raise Exception("Los animales deben pertenecer al mismo proyecto.")

    @classmethod
    def find_by_proyecto(cls,_id_proyecto):
        return FuenteExperimental.objects.filter(id_proyecto = _id_proyecto,codigoGrupoExperimental__ne= "",codigo_ne="").all()


