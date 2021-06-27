from marshmallow import ValidationError
#from servicios.commonService import CommonService
from servicios.blogProyectoService import BlogProyectoService
from schemas.blogSchema import BlogSchema,NuevoBlogSchema
from exceptions.exception import ErrorFechasInvalidas
from datetime import datetime
#from models.mongo.jaula import Jaula
#from models.mongo.experimento import Experimento
#from servicios.jaulaService import JaulaService
#from servicios.experimentoService import ExperimentoService

class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        nuevoBlog = NuevoBlogSchema().load(datos)
        return nuevoBlog
        
    @classmethod
    def convertirFecha(cls,fecha,hr,min,seg):
        #return datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%f").replace(hour=0, minute=0, second=0, microsecond=0)
        #"Sat Jun 12 2021"
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
        blogsJaula = BlogProyectoService.obtenerBlogsJaulaProyecto(id_proyecto)
        blogsExperimento = BlogProyectoService.obtenerBlogsExperimento(id_proyecto)
        return cls.busquedaPorFecha(blogsJaula+blogsExperimento,fechaDesde,fechaHasta)
