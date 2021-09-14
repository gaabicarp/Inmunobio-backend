from marshmallow import ValidationError
#from servicios.commonService import CommonService
from schemas.blogSchema import BlogSchema,NuevoBlogSchema
from datetime import datetime


class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        #falta validar usuario q crea
        return NuevoBlogSchema().load(datos)
        
    @classmethod
    def convertirFecha(cls,fecha,hr,min,seg):
        return datetime.strptime(fecha, "%a %b %d %Y").replace(hour=hr, minute=min, second=seg, microsecond=0)

    @classmethod
    def busquedaPorFecha(cls,blogs,fecDesde,fecHasta):
        fecDesde= cls.convertirFecha(fecDesde,0,0,0)
        fecHasta = cls.convertirFecha(fecHasta,23,59,0)
        cls.validarFechas(fecDesde, fecHasta)
        return cls.agregarDataUsuarios(list(filter(lambda blog: blog.fecha <= fecHasta and blog.fecha>=fecDesde , blogs)))
        
    @classmethod
    def agregarDataUsuarios(cls,blogs):
        from .commonService import CommonService
        return list(map(lambda blog: CommonService.asignarUsuario(blog), blogs))
        
    def validarFechas(fechaDesde,fechaHasta):
        if not fechaDesde<fechaHasta: raise Exception("El rango de fechas debe ser válido.")

    @classmethod
    def appendBlogs(cls,objetos):
        listaBlogs = []
        for objeto in objetos:listaBlogs.extend(objeto.blogs)
        return listaBlogs
    



