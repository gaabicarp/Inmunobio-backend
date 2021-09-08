from models.mongo.grupoExperimental import GrupoExperimental
from schemas.grupoExperimentalSchema import GrupoDeTipoOtro,DividirGrupoExperimentalOtroSchema,GrupoExperimentalSchema, AltaGrupoExperimentalSchema, DividirGrupoExperimentalSchema,AgregarFuentesAlGrupoExperimentalSchema
from models.mongo.fuenteExperimental import FuenteExperimental

class GrupoExperimentalService:

    @classmethod
    def find_by_id(cls, id):
        grupo =  GrupoExperimental.objects(id_grupoExperimental = id).first()
        if not grupo : raise Exception(f"No se encontraron grupos experimenales con id. {id}")
        return grupo

    @classmethod
    def obtenerGrupoPorId(cls,id):
        grupo = cls.find_by_id(id)
        return cls.deserializarSegunTipo(grupo)


    @classmethod
    def gruposExperimentalesDelExperimento(cls, _id_experimento):
        return GrupoExperimental.objects(id_experimento = _id_experimento).all()

    @classmethod
    def obtenerGruposExperimentalesDelExperimento(cls, _id_experimento):
        grupos = cls.gruposExperimentalesDelExperimento(_id_experimento)
        return list(map(cls.deserializarSegunTipo,grupos))

    @classmethod
    def deserializarSegunTipo(cls,grupo):
        return GrupoExperimentalSchema().dump(grupo) if grupo.tipo =="Animal" else GrupoDeTipoOtro().dump(grupo)
        
    @classmethod
    def CrearGrupoExperimental(cls, datos):
        grupoExperimental = AltaGrupoExperimentalSchema().load(datos)
        #id_experimento no hay que validarlo?
        grupoExperimental.save()

    
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
        gruposExperimentales = cls.schemaGrupoSegunTipo(datos)
        cls.elGrupoExperimentalPadreEstaHabilitado(gruposExperimentales)        
        for grupo in gruposExperimentales:
            grupo.save()
            cls.reasignarCodigoGrupoExperimentalAFuentesExperimentales(grupo,grupo.codigo)
        GrupoExperimental.objects(id_grupoExperimental = gruposExperimentales[0].parent).update(habilitado = False)  
    
    @classmethod
    def schemaGrupoSegunTipo(cls,datos):
        if datos[0]['tipo'] == 'Animal': return  DividirGrupoExperimentalSchema().load(datos, many=True) 
        return DividirGrupoExperimentalOtroSchema().load(datos, many=True)

    def elGrupoExperimentalPadreEstaHabilitado(gruposExperimentales):
        for grupo in gruposExperimentales:
            if GrupoExperimental.objects(id_grupoExperimental = grupo.parent, habilitado = True).first() is None:
                raise Exception("El grupo experimental padre debe existir y estar habilitado")

    @classmethod
    def reasignarCodigoGrupoExperimentalAFuentesExperimentales(cls,grupo,codigo):
        for fuente in grupo.fuentesExperimentales:
            FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(codigoGrupoExperimental = codigo)
    
    @classmethod
    def desasignarCodigoAFuente(cls,grupo,_codigo):
        for fuente in grupo.fuentesExperimentales:
            FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental).update(codigo = _codigo,descripcion=_codigo)

    @classmethod
    def borrarFuenteOtros(cls,grupo):
        FuenteExperimental.objects(codigoGrupoExperimental = grupo.codigo).delete()
    @classmethod
    def actualizarFuentes(cls,grupo):
        if grupo.tipo == 'Animal':
            cls.reasignarCodigoGrupoExperimentalAFuentesExperimentales(grupo, "") 
            cls.desasignarCodigoAFuente(grupo,"")
        else: 
            cls.borrarFuenteOtros(grupo)
            #las de tipo otro las borramos..

    @classmethod
    def borrarGrupoExperimental(cls,_id_grupoExperimental):
        grupo = GrupoExperimental.objects(id_grupoExperimental = _id_grupoExperimental, habilitado  =True).first()
        if not grupo:raise Exception(f"No existen grupos experimentales habilitados asociados al id.{_id_grupoExperimental}")
        cls.actualizarFuentes(grupo)
        grupo.delete()


