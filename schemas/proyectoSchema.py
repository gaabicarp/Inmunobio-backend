from marshmallow import Schema, fields, post_load, ValidationError
from models.mongo.proyecto import Proyecto
from schemas.blogSchema import NuevoBlogProyecto

class ProyectoSchema(Schema):
    id_proyecto = fields.Integer()
    codigoProyecto = fields.Str()
    nombre = fields.Str()
    descripcion = fields.Str()
    participantes = fields.List(fields.Int())
    idDirectorProyecto = fields.Int()
    fechaInicio = fields.DateTime()
    fechaFinal = fields.DateTime()
    finalizado = fields.Boolean()
    montoInicial = fields.Float()
    conclusion = fields.Str()

    #En Participantes
    #ID, Nombre y ROL

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return Proyecto(**data)
    
class ProyectoNuevoSchema(ProyectoSchema):
    codigoProyecto = fields.Str(required=True, error_messages={"required": {"message": "Se necesita el código del proyecto", "code": 400}})
    nombre = fields.Str(required=True, error_messages={"required": {"message": "Se necesita ingresar el nombre del proyecto", "code": 400}})
    montoInicial = fields.Float(required=True, error_messages={"required": {"message": "Se necesita ingresar un monto inicial", "code": 400}})
    participantes = fields.List(fields.Int(required=True, error_messages={"required": {"message": "Se deben indicar participantes", "code": 400}})) 
    idDirectorProyecto = fields.Integer(required=True, error_messages={"required": {"message": "Debe indicarse jefe de proyecto", "code": 400}})

    #TO-DO : comentar que se envia igual aunque este vacia

class ProyectoCerradoSchema(ProyectoSchema):
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto", "code:": 400}})
    conclusion = fields.Str(required=True, error_messages={"required": {"message": "Es necesario detallar la conclusión para cerrar el proyecto", "code": 400}})
    
class ProyectoModificarSchema(ProyectoSchema):
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto. Este campo no puede estar vacío", "code:": 400}})
    descripcion = fields.Str(required=True, error_messages={"required": {"message": "Es necesaria una descripcion. Este campo no puede estar vacío", "code": 400}})
    montoInicial = fields.Float(required=True, error_messages={"required": {"message": "Es necesario un montoInicial. Este campo no puede estar vacío.", "code": 400}})
    fechaFinal = fields.DateTime(allow_none=True)
    conclusion = fields.Str(allow_none=True)


class ObtenerBlogsProyectoSchema(Schema):
    fechaDesde = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-desde.", "code": 400}}) 
    fechaHasta = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-hasta", "code": 400}}) 
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto. Este campo no puede estar vacío", "code:": 400}})

class NuevoBlogProyectoSchema(Schema):
    #id obligatoria puede ser id de jaula o de exp
    id = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id", "code:": 400}})
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto. Este campo no puede estar vacío", "code:": 400}})
    blogs = fields.Nested(NuevoBlogProyecto)