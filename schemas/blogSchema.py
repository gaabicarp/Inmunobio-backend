from marshmallow import Schema, fields

class BlogSchema(Schema):
    fecha = fields.DateTime()
    detalle = fields.String()
    id_usuario = fields.Integer()
    id_blog = fields.Integer()

