  
from datetime import datetime
from models.mongo.jaula import Jaula
from models.mongo.experimento import Experimento
from servicios.jaulaService import JaulaService
from servicios.experimentoService import ExperimentoService 

class BlogProyectoService():
    @classmethod
    def blogsProyecto(cls,id_proyecto,fechaDesde,fechaHasta):
        blogsJaula = cls.obtenerBlogsJaulaProyecto(id_proyecto)
        blogsExperimento = cls.obtenerBlogsExperimento(id_proyecto)
        return cls.busquedaPorFecha(blogsJaula+blogsExperimento,fechaDesde,fechaHasta)
    
    @classmethod
    def obtenerBlogsJaulaProyecto(cls,_id_proyecto):
        jaulas = JaulaService.jaulasDelProyecto(_id_proyecto)
        #jaulas = Jaula.objects(id_proyecto = _id_proyecto).all()
        return cls.appendBlogs(jaulas)

    @classmethod
    def obtenerBlogsExperimento(cls,_id_proyecto):
        experimentos = ExperimentoService.find_all_by_id(_id_proyecto)
        #experimentos = Experimento.objects.filter(id_proyecto=_id_proyecto).all()
        return cls.appendBlogs(experimentos)

    @classmethod
    def appendBlogs(objetos ):
        listaBlogs = []
        for objeto in objetos:
            listaBlogs.append(objeto.blogs)
        return listaBlogs
    

