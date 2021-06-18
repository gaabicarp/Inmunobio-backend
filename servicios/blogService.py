from marshmallow import ValidationError
from servicios.commonService import CommonService
from schemas.blogSchema import BlogSchema,NuevoBlogSchema
from exceptions.exception import ErrorFechasInvalidas
from datetime import datetime
from models.mongo import Jaula

class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        nuevoBlog = NuevoBlogSchema().load(datos)
        return nuevoBlog

    @classmethod
    def convertirFecha(cls,fecha):
        #return datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%f").replace(hour=0, minute=0, second=0, microsecond=0)
        #"Sat Jun 12 2021"
        return datetime.strptime(fecha, "%a %b %d %Y").replace(hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def busquedaPorFecha(cls,blogs,fecDesde,fecHasta):
        fecDesde= cls.convertirFecha(fecDesde)
        print(fecDesde)
        fecHasta = cls.convertirFecha(fecHasta)
        print(fecHasta)
        cls.validarFechas(fecDesde, fecHasta)
        blogsMatch = []
        for blog in blogs:
            if blog.fecha<=fecHasta and blog.fecha>=fecDesde: blogsMatch.append(blog)
        return blogsMatch

    def validarFechas(fechaDesde,fechaHasta):
        if not fechaDesde<fechaHasta: raise ErrorFechasInvalidas()

    @classmethod
    def blogsProyecto(cls,id_proyecto,fechaDesde,fechaHasta):
        blogsJaula = cls.obtenerBlogsJaulaProyecto(id_proyecto)
        return cls.busquedaPorFecha(blogsJaula,fechaDesde,fechaHasta)
    
    @classmethod
    def obtenerBlogsJaulaProyecto(cls,_id_proyecto):
        jaulas = Jaula.objects.filter(id_proyecto=_id_proyecto)
        return jaulas.blogs