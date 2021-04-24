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

class GrupoDeTrabajoSchema(Schema):
    id_grupoDeTrabajo = fields.Integer()
    nombre = fields.Str()
    jefeDeGrupo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse Jefe de Grupo", "code": 400}}
    ) 
    integrantes = fields.List(fields.Int())
    stock = fields.Nested(StockSchema, many=True)
    grupoGral = fields.Boolean()

    @post_load
    def make_Grupo(self, data, **kwargs):
        return GrupoDeTrabajo(**data)
  

