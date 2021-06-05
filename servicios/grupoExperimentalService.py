from models.mongo.grupoExperimental import GrupoExperimental, GrupoExperimentalSchema, AltaGrupoExperimentalSchema, DividirGrupoExperimentalSchema
from models.mongo.fuenteExperimental import FuenteExperimental, FuenteExperimentalAnimalSchema, FuenteExperimentalOtroSchema
from dateutil import parser
import datetime

class GrupoExperimentalService:

    @classmethod
    def find_by_id(cls, id):
        return GrupoExperimental.objects(id_grupoExperimental = id).first().json()
    
    @classmethod
    def gruposExperimentalesDelExperimento(cls, _id_experimento):
        return GrupoExperimentalSchema().dump(GrupoExperimental.objects(id_experimento = _id_experimento).all(), many=True)

    @classmethod
    def CrearGrupoExperimental(cls, datos):
        grupoExperimental = AltaGrupoExperimentalSchema().load(datos)
        grupoExperimental.save()
    
    @classmethod
    def AgregarFuenteExperimental(cls, datos):
        #Trae el grupo experimental
        #Arma las fuetnes experimentales de tipo animal y otros

        grupoExperimentalViejo = GrupoExperimental.objects(id_grupoExperimental = datos.id_grupoExperimental).first()
        fuentesExperimentalesNuevas = map(lambda fuenteExperimental: FuenteExperimentalAnimalSchema().load(fuenteExperimental) if dato.tipo == "Animal" else FuenteExperimentalOtroSchema.load(fuenteExperimental), datos.fuentesExperimentales) 
        
        for fuenteVieja in grupoExperimentalViejo.fuentesExperimentalesNuevas:
            if any(fuenteExperimentalNueva.id_fuenteExperimental != fuenteVieja.id_fuenteExperimental for fuenteExperimentalNueva in fuentesExperimentalesNuevas):
                self.desasociarDeGrupoExperimental(fuenteVieja)
        for fuenteNueva in fuentesExperimentalesNuevas:
            if fuenteNueva.tipo == "Animal":
                self.asociarAGrupoExperimental(fuenteNueva)
            else:
                fuenteNueva.save()

    
    def desasociarDeGrupoExperimental(cls, fuenteExperimental):
        FuenteExperimental.objects(id_fuenteExperimental == fuenteExperimental.id_fuenteExperimental).update(
            codigo = "",
            codigoGrupoExperimental = ""
        )

    def asociarAGrupoExperimental(cls, fuenteExperimental):
        FuenteExperimental.objects(id_fuenteExperimental = fuenteExperimental.id_fuenteExperimental).update(
            codigo = fuenteExperimental.codigo,
            codigoGrupoExperimental = fuenteExperimental.codigoGrupoExperimental
        )
    
    @classmethod
    def dividirGrupoExperimental(cls, datos):
        gruposExperimentales = DividirGrupoExperimentalSchema().load(datos, many=True)
        cls.elGrupoExperimentalPadreEstaHabilitado(gruposExperimentales)        
        for grupo in gruposExperimentales:
            grupo.save()
            cls.reasignarCodigoGrupoExperimentalAFuentesExperimentales(grupo)
        GrupoExperimental.objects(id_grupoExperimental = gruposExperimentales[0].parent).update(habilitado = False)
    
    def elGrupoExperimentalPadreEstaHabilitado(gruposExperimentales):
        for grupo in gruposExperimentales:
            if GrupoExperimental.objects(id_grupoExperimental = grupo.parent, habilitado = True).first() is None:
                raise Exception("El grupo experimental padre debe existir y estar habilitado")

    def reasignarCodigoGrupoExperimentalAFuentesExperimentales(grupo):
        for fuente in grupo.fuentesExperimentales:
            FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(codigoGrupoExperimental = grupo.codigo)
