
from marshmallow import Schema, fields, post_load
from models.mongo.validacion import Validacion
from models.mongo.muestra import Muestra

class MuestraSchema(Schema):
    id_muestra = fields.Int()
    id_proyecto = fields.Int()
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
    id_contenedor = fields.Int()
    habilitada = fields.Boolean()
    id_fuenteExperimental = fields.Int()

    @post_load
    def make_muestra(self, data, **kwargs):
        return Muestra(**data)

class NuevaMuestraSchema(MuestraSchema):
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    id_grupoExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del grupo experimental", "code":400}})
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del experimento", "code":400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el id código de la muestra", "code": 400}})
    descripcion = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar una descripcion", "code": 400}})
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id_contenedor", "code": 400}})
    id_fuenteExperimental = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id de la fuente experimental", "code": 400}})

class ModificarMuestraSchema(MuestraSchema):
    id_muestra = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del muestra", "code":400}})
    codigo = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el id código de la muestra", "code": 400}})
    descripcion = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar una descripcion", "code": 400}})
    id_contenedor = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el codigoContenedor", "code": 400}})
    
    

