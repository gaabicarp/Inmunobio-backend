from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from flask import jsonify
from models.mongo.stock import Stock,StockSchema

class GrupoDeTrabajo(dbMongo.Document):
    id_grupoDeTrabajo = dbMongo.SequenceField()
    nombre = dbMongo.StringField()
    jefeDeGrupo = dbMongo.IntField()
    integrantes = dbMongo.ListField(dbMongo.IntField()) #ver duplicados en integrantes
    stock = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Stock'))
    grupoGral = dbMongo.BooleanField(default=False)

#schemas
class BorrarGrupoDeTrabajoSchema(Schema):
    id_grupoDeTrabajo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse id de grupo", "code": 400}}
    ) 


class ModificarGrupoDeTrabajoSchema(BorrarGrupoDeTrabajoSchema):
    integrantes = fields.List(fields.Integer,required=True,many=True,
    error_messages={"required": {"message": "Deben indicarse los miembros del grupo", "code": 400}}
    )
class jefeDeGrupoSchema(BorrarGrupoDeTrabajoSchema):
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
  

