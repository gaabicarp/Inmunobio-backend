from marshmallow import ValidationError
from servicios.commonService import CommonService
from schemas.blogSchema import BlogSchema

class BlogService():
    @classmethod
    def nuevoBlog(cls,datos):
        nuevoBlog = BlogSchema().load(datos)
        return nuevoBlog


