from marshmallow import Schema, fields, post_load
from models.mongo.validacion import Validacion
from models.mongo.experimento import Experimento
from schemas.blogSchema import BlogSchema
from schemas.muestraExternaSchema import MuestraExternaSchema 

class ExperimentoSchema(Schema):
    id_experimento = fields.Int()
    id_proyecto = fields.Int()
    codigo = fields.Str()
    fechaInicio = fields.DateTime()
    fechaFin = fields.DateTime(allow=None)
    resultados = fields.Str()
    finalizado = fields.Boolean()
    metodologia = fields.Str()
    conclusiones = fields.Str()
    objetivos = fields.Str()
    muestrasExternas = fields.Nested(MuestraExternaSchema, many=True)

    @post_load
    def make_Experimento(self, data, **kwargs):
        return Experimento(**data)

class AltaExperimentoSchema(ExperimentoSchema):
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    codigo = fields.String(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message" : "Es necesario indicar el código del experimento", "code": 400}})
    metodologia = fields.Str( required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "El campo metodología es necesario, no puede estar vacío", "code": 400}})
    objetivos = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "El campo objetivos es necesario, no puede estar vacío", "code": 400}})
class CerrarExperimentoSchema(ExperimentoSchema):
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}})
    resultados = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "El campo resultados es necesario, no puede estar vacío", "code": 400}})
    conclusiones = fields.Str(required=True, validate=Validacion.not_empty_string, error_messages={"required": {"message": "El campo resultados es necesario, no puede estar vacío", "code": 400}})
    
class ModificarExperimentoSchema(ExperimentoSchema):
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}})

class AgregarMuestrasAlExperimentoSchema(ExperimentoSchema):
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}})
    muestrasExternas = fields.Nested( MuestraExternaSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required": {"message": "El campo muestras externas no puede estar vacío", "code": 400}})
    
class NuevoBlogExpSchema(Schema):
    id_experimento = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id_experimento", "code" : 400}})
    blogs = fields.Nested(BlogSchema,required=True, error_messages={"required": {"message" : "Es necesario indicar datos de blog de jaula", "code" : 400}})

class BusquedaBlogExp(Schema):
    fechaDesde = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-desde.", "code": 400}}) 
    fechaHasta = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-hasta", "code": 400}}) 
    id_experimento = fields.Integer(required=True,error_messages={"required": {"message": "Debe indicarse  id_experimento", "code": 400}}) 
""" 
class AgregarMuestrasAlExperimentoSchema(ExperimentoSchema):
    id_proyecto = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message" : "Es necesario indicar el id del proyecto", "code": 400}})
    id_experimento = fields.Int(required=True, validate=Validacion.not_empty_int, error_messages={"required": {"message": "El campo id_experimento es necesario, no puede estar vacío", "code": 400}})
    muestrasExternas = fields.Nested( MuestraExternaSchema, many=True, required=True, validate=Validacion.not_empty_list, error_messages={"required": {"message": "El campo muestras externas no puede estar vacío", "code": 400}}) """