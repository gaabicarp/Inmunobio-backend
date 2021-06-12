from marshmallow import ValidationError
from servicios.commonService import CommonService
from schemas.blogSchema import BlogSchema,NuevoBlogSchema
from datetime import datetime

class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        nuevoBlog = NuevoBlogSchema().load(datos)
        return nuevoBlog

    @classmethod
    def convertirFecha(cls,fecha):
        return datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%S.%f").replace(hour=0, minute=0, second=0, microsecond=0)

    @classmethod
    def busquedaPorFecha(cls,blogs,fecDesde,fecHasta):
        fecDesde= cls.convertirFecha(fecDesde)
        fecHasta = cls.convertirFecha(fecHasta)
        print(fecDesde)
        print(fecHasta)
        blogsMatch = []
        for blog in blogs:
            if blog.fecha<=fecHasta and blog.fecha>=fecDesde: blogsMatch.append(blog)
        return blogsMatch



