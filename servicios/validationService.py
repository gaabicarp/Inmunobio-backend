from models.mongo.jaula import Jaula
from models.mongo.proyecto import Proyecto
from models.mongo.experimento import Experimento
from models.mongo.muestra import Muestra
from models.mongo.grupoExperimental import GrupoExperimental
from models.mongo.fuenteExperimental import FuenteExperimental

from models.mongo.contenedor import Contenedor
class ValidacionesUsuario():
    @classmethod
    def jefeDeProyecto(cls,usuario):
        if  Proyecto.objects(id_proyecto=usuario.id,finalizado= False).first():
            raise Exception(f"El usuario {usuario.nombre} es jefe de un proyecto activo. Debe desasignarse primero.")

    @classmethod
    def desvincularDeProyectos(cls,id_usuario):
        Proyecto.objects.update(pull__participantes=id_usuario)

class Validacion():

    @classmethod
    def laFuenteExperimentalPerteneceAlGrupo(cls,idFuenteExperimental,idGrupo):
        return GrupoExperimental.objects(id_grupoExperimental=idGrupo,fuentesExperimentales__id_fuenteExperimental = idFuenteExperimental ).first()
    @classmethod
    def elProyectoExiste(cls, idProyecto):
        return Proyecto.objects(id_proyecto=idProyecto).first() != None
    
    @classmethod
    def elProyectoEstaActivo(cls, idProyecto):
        return Proyecto.objects(id_proyecto=idProyecto, finalizado = False).first() != None
    
    @classmethod
    def elExperimentoExiste(cls, idExperimento):
        return Experimento.objects(id_experimento=idExperimento).first() != None
    
    @classmethod
    def elExperimentoEstaFinalizado(cls, id_experimento):
        return Experimento.objects(id_experimento = id_experimento, finalizado = False).first() != None
    
    @classmethod
    def elExperimentoPerteneceAlProyecto(cls, id_experimento, id_proyecto):
        return Experimento.objects(id_experimento = id_experimento, id_proyecto = id_proyecto).first() != None

    @classmethod
    def elExperimentoTieneLaMuestra(cls, idExperimento, idMuestra):
        return Experimento.objects(id_experimento = idExperimento, muestrasExternas__id_muestra=idMuestra).first() != None
    
    @classmethod
    def elGrupoExperimentalPerteneceAlExperimento(cls, id_experimento, id_grupoExperimental):
        return GrupoExperimental.objects(id_grupoExperimental=id_grupoExperimental, id_experimento=id_experimento).first() != None

    @classmethod
    def existeLaMuestra(cls, idMuestra):
        return Muestra.objects(id_muestra=idMuestra).first() != None
    
    @classmethod
    def laMuestraEstaHabilitada(cls, idMuestra):
        return Muestra.objects(id_muestra=idMuestra, habilitada = True).first() != None

    def existeElgrupoExperimental(grupoExperimental):
        return GrupoExperimental.objects(id_grupoExperimental=grupoExperimental.id_grupoExperimental, habilitado = True).first() != None
    
    def elGrupoExperimentalEsDelMismoTipoQueLasFuentes(grupoExperimental):
        return all(grupoExperimental.tipo == fuenteExperimental.tipo for fuenteExperimental in grupoExperimental.fuentesExperimentales)

    def todasLasFuentesTienenElMismoGrupoExperimental(grupoExperimental):
        return all(grupoExperimental.codigo == fuenteExperimental.codigoGrupoExperimental for fuenteExperimental in grupoExperimental.fuentesExperimentales)
    
    def losAnimalesEstanHabilitados(fuentesExperimentales):
        return all(FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental, baja = False).first() is not None for fuente in fuentesExperimentales)
    
    def losAnimalesNoTienenGrupoExperimental(fuentesExperimentales):
        return all(FuenteExperimental.objects(id_fuenteExperimental = fuente.id_fuenteExperimental, codigo = "", codigoGrupoExperimental = "").first() is not None for fuente in fuentesExperimentales)
    
    def losAnimalesPertenecenAlMismoProyectoDelExperimento(grupoExperimental):
        experimento = Experimento.objects(id_experimento = grupoExperimental.id_experimento).first()
        return all(experimento.id_proyecto == animal.id_proyecto for animal in grupoExperimental.fuentesExperimentales)
    
    def elContenedorTieneContenedoresHijos(idContenedor):
        contenedores = Contenedor.objects(parent = idContenedor).all()
        return len(contenedores) != 0
    
    def elContenedorTieneMuestrasAsociadas(idContenedor):
        muestras = Muestra.objects(id_contenedor = idContenedor).all()
        return len(muestras) != 0
    
    def elContenedorExiste(idContenedor):
        return Contenedor.objects(id_contenedor = idContenedor).first() != None
    
    def elContenedorPadreEstaDisponible(contenedor):
        return Contenedor.objects(id_contenedor = contenedor.parent, disponible = True).first() != None
    
"""     def existeLaJaulas(idJaula):
        jaula = Jaula.objects(id_jaula = idJaula, habilitado = True).first()
        return jaula != None """