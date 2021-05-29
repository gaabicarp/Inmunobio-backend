from models.mongo.fuenteExperimental import AnimalSchema, FuenteExperimental, FuenteExperimentalSchema, NuevoAnimalSchema
from models.mongo.grupoExperimental import GrupoExperimental
from dateutil import parser
import datetime

class FuenteExperimentalService:

    @classmethod
    def find_by_id(cls, idFuenteExperimental):
        return FuenteExperimentalSchema().dump(FuenteExperimental.objects(id_fuenteExperimental = idFuenteExperimental).first())
    
    @classmethod
    def find_by_codigo(cls, codigoFuenteExperimental):
        return FuenteExperimentalSchema().dump(FuenteExperimental.objects(codigo = codigoFuenteExperimental).first())

    @classmethod
    def find_all_sin_asignar(cls):
        return FuenteExperimentalSchema().dump(FuenteExperimental.objects(tipo="Animal", grupoExperimental="").all(), many=True)
    
    #Consultar qué datos se piden cuando se carga el animal y cuáles cuando se crea una nueva fuente experimental
#    @classmethod
#    def nuevaFuenteExperimental(cls, datos):
#        fuentesExperimentales = map(lambda dato: NuevaFuenteExperimentalOtroSchema().load(dato) if dato.tipo == "Animal" else NuevaFuenteExperimentalOtroSchema.load(dato), fuentesExperimentales) 
#        for fuente in fuentesExperimentales:
#            if fuente.tipo != "Animal":
#                fuente.save()
#            else:
#                FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(
#                    codigo = fuente.codigo,
#                    codigoGrupoExperimental = fuente.codigoGrupoExperimental
#                )
#        cls.actualizarFuentesExperimentalesEnGrupoExperimental(fuentesExperimentales[0].codigoGrupoExperimental)
    
    def actualizarFuentesExperimentalesEnGrupoExperimental(cls, codigoGrupoExperimental):
        fuentesExperimentales =  FuenteExperimental.objects(codigoGrupoExperimental = codigoGrupoExperimental).all()
        GrupoExperimental.objects(codigo = codigoGrupoExperimental).update(
            fuentesExperimentales = fuentesExperimentales
        )

    @classmethod
    def desvincularFuenteExperimental(cls, datos):
        pass


