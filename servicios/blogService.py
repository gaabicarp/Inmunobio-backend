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
        print("fecha desde ahsta:")
        print(fecDesde,fecHasta)
        cls.validarFechas(fecDesde, fecHasta)
        blogsMatch = []
        for blog in blogs:
            print("blog fecha iteracion",blog.fecha)
            if blog.fecha <= fecHasta and blog.fecha>=fecDesde: blogsMatch.append(blog)
        print(blogsMatch)
        return blogsMatch

    def validarFechas(fechaDesde,fechaHasta):
        if not fechaDesde<fechaHasta: raise ErrorFechasInvalidas()


    @classmethod
    def appendBlogs(cls,objetos):
        listaBlogs = []
        for objeto in objetos:listaBlogs.extend(objeto.blogs)
        return listaBlogs
    



