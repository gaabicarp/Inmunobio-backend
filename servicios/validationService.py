from models.mongo.proyecto import Proyecto
from models.mongo.experimento import Experimento
from models.mongo.muestra import Muestra
from models.mongo.grupoExperimental import GrupoExperimental
class ValidacionesUsuario():
    @classmethod
    def desvincularDeProyectos(cls,id_usuario):
        proyectos = Proyecto.objects.update(pull__participantes=id_usuario)

class Validacion():

    @classmethod
    def elProyectoExiste(cls, idProyecto):
        return Proyecto.objects(id_proyecto=idProyecto).first() != None
    
    @classmethod
    def elExperimentoEstaFinalizado(cls, id_experimento):
        return Experimento.objects(id_experimento = id_experimento, finalizado = False).first() != None
    
    @classmethod
    def elExperimentoPerteneceAlProyecto(cls, id_experimento, id_proyecto):
        return Experimento.objects(id_experimento = id_experimento, id_proyecto = id_proyecto).first() != None
    
    @classmethod
    def elGrupoExperimentalPerteneceAlExperimento(cls, id_experimento, id_grupoExperimental):
        return GrupoExperimental.objects(id_grupoExperimental=id_grupoExperimental, id_experimento=id_experimento).first() != None

    @classmethod
    def existeLaMuestra(self, idMuestra):
        return Muestra.objects(id_muestra=idMuestra).first() != None
    
    @classmethod
    def laMuestraEstaHabilitada(self, idMuestra):
        return Muestra.objects(id_muestra=idMuestra, habilitada = True).first() != None