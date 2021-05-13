from models.mongo.grupoDeTrabajo import GrupoDeTrabajo
from schemas.stockSchema import StockSchema,NuevoStockSchema
from marshmallow import Schema, fields, post_load

#schemas
class GrupoDeTrabajoIDSchema(Schema):
    id_grupoDeTrabajo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse id de grupo", "code": 400}}
    ) 

class ModificarGrupoDeTrabajoSchema(GrupoDeTrabajoIDSchema):
    integrantes = fields.List(fields.Integer,required=True,many=True,
    error_messages={"required": {"message": "Deben indicarse los miembros del grupo", "code": 400}}
    )
class jefeDeGrupoSchema(GrupoDeTrabajoIDSchema):
    jefeDeGrupo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse id jefe de grupo", "code": 400}}
    ) 
  
class GrupoDeTrabajoSchema(Schema):
    id_grupoDeTrabajo = fields.Integer()
    nombre = fields.Str()
    jefeDeGrupo = fields.Integer()
    integrantes = fields.List(fields.Int())
    stock = fields.Nested(StockSchema, many=True)
    grupoGral = fields.Boolean()
  
class NuevoGrupoDeTrabajoSchema(Schema):
    nombre = fields.Str(required=True,
    error_messages={"required": {"message": "Debe indicarse nombre de grupo", "code": 400}}
    ) 
    jefeDeGrupo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse Jefe de Grupo", "code": 400}}
    ) 
    grupoGral = fields.Boolean(default=False)

    @post_load
    def make_Grupo(self, data, **kwargs):
        return GrupoDeTrabajo(**data)
  

class NuevoStockGrupoSchema(GrupoDeTrabajoIDSchema):
    stock = fields.Nested(NuevoStockSchema)
  
class busquedaStocksSchema(GrupoDeTrabajoIDSchema):
    id_espacioFisico = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_stock", "code": 400}})
    id_productoEnStock = fields.Integer(required=True, error_messages={"required": {"message" : "Debe indicarse id_productoEnStock", "code": 400}})
