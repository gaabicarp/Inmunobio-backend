from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from flask import jsonify
from models.mongo.stock import Stock,StockSchema

class GrupoDeTrabajo(dbMongo.Document):
    idGrupoDeTrabajo = dbMongo.SequenceField()
    nombre = dbMongo.StringField()
    jefeDeGrupo = dbMongo.IntField()
    integrantes = dbMongo.ListField(dbMongo.IntField()) #ver duplicados en integrantes
    stock = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Stock'))
 
class GrupoDeTrabajoSchema(Schema):
    idGrupoDeTrabajo = fields.Integer()
    nombre = fields.Str()
    jefeDeGrupo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse Jefe de Grupo", "code": 400}}
    ) 
    integrantes = fields.List(fields.Int())
    stock = fields.Nested(StockSchema, many=True)

    @post_load
    def make_Grupo(self, data, **kwargs):
        return GrupoDeTrabajo(**data)
  

