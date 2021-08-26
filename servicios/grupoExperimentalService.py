from resources.experimentoResource import Experimentos
from models.mongo.grupoExperimental import GrupoExperimental
from schemas.grupoExperimentalSchema import GrupoExperimentalSchema, AltaGrupoExperimentalSchema, DividirGrupoExperimentalSchema,AgregarFuentesAlGrupoExperimentalSchema
from models.mongo.fuenteExperimental import FuenteExperimental
from schemas.fuenteExperimentalSchema import  FuenteExperimentalAnimalSchema, FuenteExperimentalOtroSchema

class GrupoExperimentalService:

    @classmethod
    def find_by_id(cls, id):
        grupo =  GrupoExperimental.objects(id_grupoExperimental = id).first()
        if not grupo : raise Exception(f"No se encontraron grupos experimenales con id. {id}")
        return grupo

    @classmethod
    def gruposExperimentalesDelExperimento(cls, _id_experimento):
        return GrupoExperimental.objects(id_experimento = _id_experimento).all()

    @classmethod
    def CrearGrupoExperimental(cls, datos):
        grupoExperimental = AltaGrupoExperimentalSchema().load(datos)
        #id_experimento no hay que validarlo?
        grupoExperimental.save()
    
    """ @classmethod
    def AgregarFuenteExperimental(cls, datos):
        #Trae el grupo experimental
        #Arma las fuetnes experimentales de tipo animal y otros

        grupoExperimentalViejo = GrupoExperimental.objects(id_grupoExperimental = datos.id_grupoExperimental).first()
        fuentesExperimentalesNuevas = map(lambda fuenteExperimental: FuenteExperimentalAnimalSchema().load(fuenteExperimental) if dato.tipo == "Animal" else FuenteExperimentalOtroSchema.load(fuenteExperimental), datos.fuentesExperimentales) 
        for fuenteVieja in grupoExperimentalViejo.fuentesExperimentalesNuevas:
            if any(fuenteExperimentalNueva.id_fuenteExperimental != fuenteVieja.id_fuenteExperimental for fuenteExperimentalNueva in fuentesExperimentalesNuevas):
                cls.desasociarDeGrupoExperimental(fuenteVieja)
        for fuenteNueva in fuentesExperimentalesNuevas:
            if fuenteNueva.tipo == "Animal":
                cls.asociarAGrupoExperimental(fuenteNueva)
            else:
                fuenteNueva.save() """

    
    def desasociarDeGrupoExperimental(cls, fuenteExperimental):
        FuenteExperimental.objects(id_fuenteExperimental = fuenteExperimental.id_fuenteExperimental).update(
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
            cls.reasignarCodigoGrupoExperimentalAFuentesExperimentales(grupo,grupo.codigo)
        print(GrupoExperimental.objects(id_grupoExperimental = gruposExperimentales[0].parent))
        GrupoExperimental.objects(id_grupoExperimental = gruposExperimentales[0].parent).update(habilitado = False)
    
    def elGrupoExperimentalPadreEstaHabilitado(gruposExperimentales):
        for grupo in gruposExperimentales:
            if GrupoExperimental.objects(id_grupoExperimental = grupo.parent, habilitado = True).first() is None:
                raise Exception("El grupo experimental padre debe existir y estar habilitado")

    @classmethod
    def reasignarCodigoGrupoExperimentalAFuentesExperimentales(cls,grupo,codigo):
        for fuente in grupo.fuentesExperimentales:
            FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(codigoGrupoExperimental = codigo)
    
    @classmethod
    def reasignarCodigoFuente(cls,grupo,_codigo):
        for fuente in grupo.fuentesExperimentales:
            FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(codigo = _codigo)

    @classmethod
    def borrarGrupoExperimental(cls,_id_grupoExperimental):
        #GrupoExperimental.objects(id_grupoExperimental = idGrupoPadre,parent=idGrupoPadre).delete()
        grupo = GrupoExperimental.objects(id_grupoExperimental = _id_grupoExperimental, habilitado  =True).first()
        if not grupo:raise Exception(f"No existen grupos experimentales habilitados asociados al id.{_id_grupoExperimental}")
        #borra nodo padre y todas sus ramas, ¿pero que pasa con los grupos anteriores que esta "deshabilitados?"
        #gruposHijos = GrupoExperimental.objects(parent = _id_grupoExperimental, habilitado  =True)
        #if gruposHijos :
        #[cls.borrarGrupoExperimental(grupoHijo.id_grupoExperimental) for grupoHijo in gruposHijos]
        #grupos = GrupoExperimental.objects(parent = idGrupoPadre)
        cls.reasignarCodigoGrupoExperimentalAFuentesExperimentales(grupo, "") 
        cls.reasignarCodigoFuente(grupo,"")
        grupo.delete()


