from models.mongo.validacion import Validacion
from marshmallow import Schema, fields, post_load
from models.mongo.contenedor import Contenedor

class ContenedorSchema(Schema):
    id_contenedor = fields.Int()
    codigo = fields.Str()
    nombre = fields.Str()
    descripcion = fields.Str()
    temperatura = fields.Str()
    id_proyecto = fields.Int()
    capacidad = fields.Int()
    fichaTecnica = fields.Str()
    disponible = fields.Boolean()
    parent = fields.Int()
    id_espacioFisico = fields.Int()
    
    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Contenedor(**data)

class ContenedorNuevoSchema(ContenedorSchema):
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el código para el contenedor", "code": 400}})
    nombre = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el nombre para el contenedor", "code": 400}})
    id_espacioFisico = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del espacio fisico en dónde se encuentra", "code": 400}})


class ContenedorProyectoSchema(ContenedorSchema):
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del contenedor", "code": 400}})
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    id_espacioFisico = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del espacio fisico en dónde se encuentra", "code": 400}})

class ContenedorPrincipalSchema(ContenedorSchema):
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el ID del contenedor", "code": 400}})

class ContenedorParentSchema(ContenedorSchema):
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el ID del contenedor", "code": 400}})
    parent = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el ID del contenedor principal en el parent", "code": 400}})

class ModificarContenedorSchema(ContenedorSchema):
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el ID del contenedor.", "code": 400}})
