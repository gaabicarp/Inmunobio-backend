from marshmallow import ValidationError
from servicios.commonService import CommonService
from schemas.blogSchema import BlogSchema,NuevoBlogSchema

class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        nuevoBlog = NuevoBlogSchema().load(datos)
        return nuevoBlog


