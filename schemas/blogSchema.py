from marshmallow import Schema, fields,post_load
from models.mongo.blog import Blog

class NuevoBlogSchema(Schema):
    fecha = fields.DateTime()
    detalle = fields.String()
    id_usuario = fields.Integer()
    tipo = fields.String()

    @post_load
    def makeBlog(self, data, **kwargs):
        return Blog(**data)


class BlogSchema(NuevoBlogSchema):
    fecha = fields.DateTime()
    detalle = fields.String()
    id_usuario = fields.Integer()
    id_blog = fields.Integer(dump_only=True)
    tipo = fields.String()