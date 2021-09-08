from servicios.commonService import CommonService
from models.mongo.grupoExperimental import GrupoExperimental
from models.mongo.muestra import Muestra
from schemas.muestraSchema import  MuestraSchema, NuevaMuestraSchema, ModificarMuestraSchema
from schemas.muestrPropiaSchema import  MuestraPropiaSchema
from models.mongo.experimento import Experimento
from schemas.experimentoSchema import AgregarMuestrasAlExperimentoSchema
from .validationService import Validacion
from dateutil import parser
import datetime

class MuestraService:

    @classmethod
    def find_by_id(cls, idMuestra):
        return Muestra.objects.filter(id_muestra=idMuestra).first()

    # @classmethod
    # def find_all_by_experimento(cls, idExperimento):
    #     muestras = Muestra.objects.filter(id_experimento=idExperimento).all()
    #     return MuestraSchema.dump(muestras, many=True)
    
    @classmethod
    def find_all_by_grupoExperimental(cls, idGrupoExperimental):
        return Muestra.objects(id_grupoExperimental=idGrupoExperimental, habilitada = True).all()

    @classmethod
    def find_all_by_proyecto(cls, idProyecto):
        return Muestra.objects(id_proyecto=idProyecto, habilitada = True).all()

    @classmethod
    def muestrasDelExperimentoDatosExtra(cls,muestras):      
        [CommonService.asignarNombreExperimento(CommonService.asignarNombreContenedorAux(muestra)) for muestra in muestras ]

    @classmethod
    def nuevasMuestras(cls, datos):
        muestras = NuevaMuestraSchema().load(datos, many=True)
        cls.validarRelacionDeMuestras(cls, muestras)
        for muestra in muestras: muestra.save()
        cls.actualizarMuestrasEnGrupoExperimental(muestras[0].id_grupoExperimental)
    
    def validarRelacionDeMuestras(self, muestras):
        for muestra in muestras:
            if not Validacion().elProyectoExiste(muestra.id_proyecto):
                raise Exception(f"El proyecto con id {muestra.id_proyecto} no existe.")
            if not Validacion().elExperimentoEstaFinalizado(muestra.id_experimento):
                raise Exception(f"El experimento con id {muestra.id_experimento} está finalizado.")
            if not Validacion().elExperimentoPerteneceAlProyecto(muestra.id_experimento, muestra.id_proyecto):
                raise Exception(f"El experimento con id {muestra.id_experimento} no pertenece al proyecto con id {muestra.id_proyecto}")
            if not Validacion().elGrupoExperimentalPerteneceAlExperimento(muestra.id_experimento, muestra.id_grupoExperimental):
                raise Exception(f"El grupo experimental con id {muestra.id_grupoExperimental} no pertenece al experimento con id {muestra.id_experimento}")
            if not Validacion().laFuenteExperimentalPerteneceAlGrupo(muestra.id_fuenteExperimental, muestra.id_grupoExperimental):
                raise Exception(f"La fuente experimental con id {muestra.id_fuenteExperimental} no pertenece al grupo experimental con id {muestra.id_grupoExperimental}")

    def actualizarMuestrasEnGrupoExperimental(idGrupoExperimental):
        muestras = Muestra.objects.filter(id_grupoExperimental=idGrupoExperimental, habilitada = True).all()
        muestrasPropiasDict = MuestraSchema(exclude=['id_contenedor', 'id_grupoExperimental', 'id_experimento', 'id_proyecto', 'habilitada']).dump(muestras, many=True)
        muestrasPropias = MuestraPropiaSchema().load(muestrasPropiasDict, many=True)
        GrupoExperimental.objects(id_grupoExperimental= idGrupoExperimental).update(muestras = muestrasPropias)
    
    def removerMuestraExternaDelExperimento(muestra):
        Experimento.objects(muestrasExternas__id_muestra=muestra.id_muestra).update(pull__muestrasExternas__id_muestra=muestra.id_muestra)
        
    def validarMuestra(idMuestra):
        if not Validacion().existeLaMuestra(idMuestra):
            raise Exception(f"No existe muestra con el id {idMuestra}.")
        if not Validacion().laMuestraEstaHabilitada(idMuestra):
            raise Exception(f"La muestra con id {idMuestra} se encuentra deshabilitada.")

    @classmethod
    def modificarMuestra(cls, datos):
        muestra = ModificarMuestraSchema().load(datos)
        cls.validarMuestra(muestra.id_muestra)
        Muestra.objects(id_muestra = muestra.id_muestra).update(
            codigo = muestra.codigo,
            descripcion = muestra.descripcion,
            id_contenedor = muestra.id_contenedor
        )
        cls.modificarMuestraEnGrupoExperimental(cls, muestra)
    
    def modificarMuestraEnGrupoExperimental(self, muestra):
        GrupoExperimental.objects(id_grupoExperimental=muestra.id_grupoExperimental, muestras__id_muestra=muestra.id_muestra).update(
            set__muestras__S__codigo=muestra.codigo, 
            set__muestras__S__descripcion=muestra.descripcion)

    #Falta agregar la actualización en experimentos
    @classmethod
    def darDeBajaMuestra(cls, idMuestra):
        cls.validarMuestra(idMuestra)
        muestra = Muestra.objects(id_muestra=idMuestra).first()
        Muestra.objects(id_muestra = idMuestra).update(habilitada = False)
        cls.actualizarMuestrasEnGrupoExperimental(muestra.id_grupoExperimental)
        cls.removerMuestraExternaDelExperimento(muestra)
    
    @classmethod
    def obtenerMuestrasDeFuente(cls,_id_fuente):
        muestras = MuestraSchema().dump(Muestra.objects(id_fuenteExperimental=_id_fuente).all(),many=True)
        for muestra in muestras: 
            CommonService.asignarNombreContenedorAux(muestra)
        return  muestras

    def agregarMuestrasExternasAlExperimento(cls, datos):
        experimento = AgregarMuestrasAlExperimentoSchema().load(datos)
        cls.validarMuestrasExternas(cls, experimento)
        Experimento.objects(id_experimento = experimento.id_experimento).update(muestrasExternas=experimento.muestrasExternas)