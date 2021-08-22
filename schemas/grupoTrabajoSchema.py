from models.mongo.grupoDeTrabajo import GrupoDeTrabajo
from marshmallow import Schema, fields, post_load
from models.mongo.validacion import Validacion


class jefeDeGrupoSchema(Schema):
    id_grupoDeTrabajo = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse id de grupo", "code": 400}}) 
    jefeDeGrupo = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse id jefe de grupo", "code": 400}}) 
  
class GrupoDeTrabajoSchema(Schema):
    id_grupoDeTrabajo = fields.Integer()
    nombre = fields.Str()
    jefeDeGrupo = fields.Integer()
    integrantes = fields.List(fields.Int())
    grupoGral = fields.Boolean(default=False)

    @post_load
    def make_Grupo(self, data, **kwargs):
        return GrupoDeTrabajo(**data)

class NuevoGrupoDeTrabajoSchema(GrupoDeTrabajoSchema):
    nombre = fields.Str(required=True,validate=Validacion.not_empty_string,error_messages={"required": {"message": "Debe indicarse nombre de grupo", "code": 400}}) 
    jefeDeGrupo = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse Jefe de Grupo", "code": 400}}) 
    
class GrupoDeTrabajoDatosExtra(GrupoDeTrabajoSchema):
    from .usuarioSchema import UsuarioSchema
    jefeDeGrupo = fields.Nested(UsuarioSchema)
    integrantes = fields.Nested(UsuarioSchema, many=True)
    
class ModificarGrupoDeTrabajoSchema(NuevoGrupoDeTrabajoSchema):
    id_grupoDeTrabajo = fields.Integer(required=True,validate=Validacion.not_empty_int,error_messages={"required": {"message": "Debe indicarse id de grupo", "code": 400}}) 

