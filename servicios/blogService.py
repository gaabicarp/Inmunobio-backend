from marshmallow import ValidationError
#from servicios.commonService import CommonService
from schemas.blogSchema import BlogSchema,NuevoBlogSchema
from exceptions.exception import ErrorFechasInvalidas
from datetime import datetime


class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        #falta validar usuario q crea
        nuevoBlog = NuevoBlogSchema().load(datos)
        return nuevoBlog
        
    @classmethod
    def convertirFecha(cls,fecha,hr,min,seg):
        return datetime.strptime(fecha, "%a %b %d %Y").replace(hour=hr, minute=min, second=seg, microsecond=0)

    @classmethod
    def busquedaPorFecha(cls,blogs,fecDesde,fecHasta):
        fecDesde= cls.convertirFecha(fecDesde,0,0,0)
        fecHasta = cls.convertirFecha(fecHasta,23,59,0)
        cls.validarFechas(fecDesde, fecHasta)
        blogsMatch = []
        for blog in blogs:
            if blog.fecha <= fecHasta and blog.fecha>=fecDesde: blogsMatch.append(blog)
        return blogsMatch

    def validarFechas(fechaDesde,fechaHasta):
        if not fechaDesde<fechaHasta: raise ErrorFechasInvalidas()

    @classmethod
    def blogsProyecto(cls,id_proyecto,fechaDesde,fechaHasta):
        blogsJaula = cls.obtenerBlogsJaulaProyecto(id_proyecto)
        blogsExperimento = cls.obtenerBlogsExperimento(id_proyecto)
        return cls.busquedaPorFecha(blogsJaula+blogsExperimento,fechaDesde,fechaHasta)


    @classmethod
    def obtenerBlogsJaulaProyecto(cls,_id_proyecto):
        from servicios.jaulaService import JaulaService
        jaulas = JaulaService.jaulasDelProyecto(_id_proyecto)
        return cls.appendBlogs(jaulas)

    @classmethod
    def obtenerBlogsExperimento(cls,_id_proyecto):
        from servicios.experimentoService import ExperimentoService 
        experimentos = ExperimentoService.find_all_by_id(_id_proyecto)
        return cls.appendBlogs(experimentos)

    @classmethod
    def appendBlogs(cls,objetos):
        listaBlogs = []
        for objeto in objetos:listaBlogs.extend(objeto.blogs)
        return listaBlogs
    



