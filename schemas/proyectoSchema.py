from marshmallow import Schema, fields, post_load, ValidationError
from models.proyecto import Proyecto

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

class ProyectoCerradoSchema(ProyectoSchema):
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto", "code:": 400}})
    conclusion = fields.Str(required=True, error_messages={"required": {"message": "Es necesario detallar la conclusión para cerrar el proyecto", "code": 400}})
    
class ProyectoModificarSchema(ProyectoSchema):
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto. Este campo no puede estar vacío", "code:": 400}})
    descripcion = fields.Str(required=True, error_messages={"required": {"message": "Es necesaria una descripcion. Este campo puede estar vacío", "code": 400}})
    montoInicial = fields.Float(required=True, error_messages={"required": {"message": "Es necesario un montoInicial. Este campo no puede estar vacío.", "code": 400}})


class ObtenerBlogsProyectoSchema(Schema):
    fechaDesde = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-desde.", "code": 400}}) 
    fechaHasta = fields.String(required=True,error_messages={"required": {"message": "Debe indicarse  fecha-hasta", "code": 400}}) 
    id_proyecto = fields.Integer(required=True, error_messages={"required": {"message": "Es necesario el id_proyecto. Este campo no puede estar vacío", "code:": 400}})
