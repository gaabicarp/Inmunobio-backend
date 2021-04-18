from models.mongo.experimento import Experimento, ExperimentoSchema, ExperimentoModificarGruposExperimentalesSchema, AltaExperimentoSchema, CerrarExperimentoSchema
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
    def modificarGruposExperimentalesDelExperimento(cls, datos):
        ExperimentoModificarGruposExperimentalesSchema().load(datos)
        experimento = Experimento.objects.filter(id_experimento=datos['id_experimento']).first()
        experimento.update(gruposExperimentales=datos['gruposExperimentales'])