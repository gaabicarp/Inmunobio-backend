from marshmallow import Schema, fields,post_load,ValidationError
from models.mongo.blog import Blog
from models.mongo.validacion import Validacion


class NuevoBlogSchema(Schema):
    fecha = fields.DateTime()
    detalle = fields.String(required=True,validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario dar detalle del blog", "code" : 400}})
    id_usuario = fields.Integer(required=True,validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del usuario autor", "code" : 400}})
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

class BlogSchemaExtendido(BlogSchema):
    from .usuarioSchema import UsuarioSchema
    id_usuario = fields.Nested(UsuarioSchema)

def tipoValidacion(data):
    if( data != "Jaula" and data != "Experimento"):
        raise ValidationError('Debe indicarse como tipo "Jaula" o "Experimento"')

class NuevoBlogProyecto(NuevoBlogSchema):
    tipo = fields.String(required=True, error_messages={"required": {"message" : "Es necesario indicar tipo de blog", "code" : 400}},validate = tipoValidacion)

