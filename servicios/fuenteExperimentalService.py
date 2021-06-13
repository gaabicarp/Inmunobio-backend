from models.mongo.fuenteExperimental import FuenteExperimental, FuenteExperimentalSchema, FuenteExperimentalAnimalSchema, FuenteExperimentalOtroSchema
from models.mongo.grupoExperimental import GrupoExperimental, AgregarFuentesAlGrupoExperimentalSchema
from dateutil import parser
import datetime

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
        cls.validarGrupoExperimental(cls, grupoExperimental)
        if fuentesExperimentales[0].tipo == "Animal":
            cls.validarAnimales(cls, fuentesExperimentales)
            cls.nuevasFuentesAnimales(fuentesExperimentales)
        else:
            cls.nuevasFuentesOtros(fuentesExperimentales)
        cls.actualizarFuentesExperimentalesEnGrupoExperimental(grupoExperimental)
        return {"Status" : "Se crearon las fuentes experimentales",}, 200
    
    def nuevasFuentesAnimales(fuentesExperimentales):
        for fuente in fuentesExperimentales:
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
        fuentesExperimentalesDic = FuenteExperimentalSchema(exclude=['id_jaula', 'baja']).dump(fuentesExperimentales, many=True)
        GrupoExperimental.objects(id_grupoExperimental = grupoExperimental.id_grupoExperimental).update(
            fuentesExperimentales = fuentesExperimentalesDic
        )

    def existeElgrupoExperimental(grupoExperimental):
        res = GrupoExperimental.objects(id_grupoExperimental=grupoExperimental.id_grupoExperimental, habilitado = True).first()
        return res != None

    def elGrupoExperimentalEsDelMismoTipoQueLasFuentes(grupoExperimental):
        for fuenteExperimental in grupoExperimental.fuentesExperimentales:
            if grupoExperimental.tipo != fuenteExperimental.tipo:
                return False
        return True
    
    def todasLasFuentesTienenElMismoGrupoExperimental(grupoExperimental):
        for fuenteExperimental in grupoExperimental.fuentesExperimentales:
            if grupoExperimental.codigo != fuenteExperimental.codigoGrupoExperimental:
                return False
        return True
    
    def losAnimalesEstanHabilitados(fuentesExperimentales):
        return all(FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental, baja = False).first() is not None for fuente in fuentesExperimentales)
            
    def losAnimalesNoTienenGrupoExperimental(fuentesExperimentales):
        return all(FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental, codigo = "", codigoGrupoExperimental = "").first() is not None for fuente in fuentesExperimentales)

    def validarGrupoExperimental(self, grupoExperimental):
        if not self.existeElgrupoExperimental(grupoExperimental):
            raise Exception("El grupo experimental debe existir y estar habilitado")
        if not self.elGrupoExperimentalEsDelMismoTipoQueLasFuentes(grupoExperimental):
            raise Exception("El grupo experimental y las fuentes tienen que ser del mismo tipo")
        if not self.todasLasFuentesTienenElMismoGrupoExperimental(grupoExperimental):
            raise Exception("Todas las fuentes experimentales deben tener el mismo código de grupo experimental.")
    
    def validarAnimales(self, fuentesExperimentales):
        if not self.losAnimalesEstanHabilitados(fuentesExperimentales):
            raise Exception("Los animales deben existir y no pueden estar en estado de baja.")
        if not self.losAnimalesNoTienenGrupoExperimental(fuentesExperimentales):
            raise Exception("Los animales ya están en uso.")



