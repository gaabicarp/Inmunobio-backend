from .validationService import Validacion
from models.mongo.experimento import Experimento, ExperimentoSchema, ModificarExperimentoSchema, AltaExperimentoSchema, CerrarExperimentoSchema, AgregarMuestrasAlExperimentoSchema
from servicios.muestraService import MuestraService
from dateutil import parser
import datetime

class ExperimentoService:    

    @classmethod
    def find_by_id(cls, idExperimento):
        return Experimento.objects.filter(id_experimento=idExperimento).first()

    @classmethod
    def find_all_by_idProyecto(cls, idProyecto):
        return ExperimentoSchema().dump(Experimento.objects.filter(id_proyecto=idProyecto).all(), many=True)

    @classmethod
    def nuevoExperimento(cls, datos):
        experimento = AltaExperimentoSchema().load(datos)
        experimento.save()
    
    @classmethod
    def cerrarExperimento(cls, datos):
        experimento = CerrarExperimentoSchema().load(datos)
        Experimento.objects(id_experimento=experimento.id_experimento).update(
            fechaFin = parser.parse(str(datetime.datetime.utcnow())),
            resultados = experimento.resultados,
            finalizado = True,
            conclusiones = experimento.conclusiones
        )
    
    @classmethod
    def modificarExperimento(cls, datos):
        experimento = ModificarExperimentoSchema().load(datos)
        Experimento.objects(id_experimento=experimento.id_experimento).update(
            resultados= experimento.resultados,
            metodologia = experimento.metodologia,
            objetivos = experimento.objetivos,
            muestrasExternas = experimento.muestrasExternas
        )

    def lasMuestrasSonDelMismoProyectoDelExperimento(self, experimento):
        return all(experimento.id_proyecto == muestraExterna.id_proyecto for muestraExterna in experimento.muestrasExternas)
    
    def lasMuestrasEstanHabilitadas(self, experimento):
        return all(MuestraService.validarMuestra(muestra.id_muestra) for muestra in experimento.muestrasExternas)

    def validarMuestrasExternas(self, experimento):
        if self.lasMuestrasSonDelMismoProyectoDelExperimento(self, experimento):
            raise ValueError("Todas las muestras tienen que ser del mismo proyecto.")
        if self.lasMuestrasEstanHabilitadas(self, experimento):
            raise ValueError("Todas las muestras tienen que estar habilitadas.")

    @classmethod
    def agregarMuestrasExternasAlExperimento(cls, datos):
        experimento = AgregarMuestrasAlExperimentoSchema().load(datos)
        cls.validarMuestrasExternas(cls, experimento)
        Experimento.objects(id_experimento = experimento.id_experimento).update(muestrasExternas=experimento.muestrasExternas)

    @classmethod
    def removerMuestraDeExperimento(cls, idExperimento, idMuestra):
        cls.validarRemoverMuestraExperimento(idExperimento, idMuestra)
        Experimento.objects(id_experimento=idExperimento).update(pull__muestrasExternas__id_muestra=idMuestra)
    
    def validarRemoverMuestraExperimento(idExperimento, idMuestra):
        if not Validacion().elExperimentoExiste(idExperimento):
            raise Exception(f"El experimento con id {idExperimento} no existe.")
        if not Validacion().existeLaMuestra(idMuestra):
            raise Exception(f"La muestra con id {idMuestra} no existe.")
        if not Validacion().elExperimentoTieneLaMuestra(idExperimento, idMuestra):
            raise Exception(f"El experimento con id {idExperimento} no tiene la muestra con id {idMuestra}.")