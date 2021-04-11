from db import dbMongo
from marshmallow import Schema, fields, post_load, ValidationError
from flask import jsonify

class Stock(dbMongo.EmbeddedDocument):
    lote = dbMongo.StringField()#Charlar stock y lote
    detalleUbicacion = dbMongo.StringField()
    unidad = dbMongo.IntField()
    fechaVencimiento = dbMongo.DateTimeField()
    id_espacioFisico = dbMongo.IntField()
    codigoContenedor = dbMongo.StringField()

class GrupoDeTrabajo(dbMongo.Document):
    idGrupoDeTrabajo = dbMongo.SequenceField()
    nombre = dbMongo.StringField()
    jefeDeGrupo = dbMongo.IntField()
    integrantes = dbMongo.ListField(dbMongo.IntField())
    stock = dbMongo.ListField(dbMongo.EmbeddedDocumentField(Stock))

    @classmethod
    def find_by_id(cls, id):
        return cls.objects.filter(idGrupoDeTrabajo=id).first()

    @classmethod
    def find_by_nombre(cls, _nombre):
        return cls.objects(nombre = _nombre).first()
    @classmethod
    def modificarMiembros(cls, datos):
        #Se pasa una lista de los nuevos miembros, y se pisa la anterior
        if 'integrantes' in datos:
            cls.objects(idGrupoDeTrabajo=datos['id']).update_one(integrantes=datos['integrantes'])
        if 'jefeDeGrupo' in datos:
            cls.objects(idGrupoDeTrabajo=datos['id']).update_one(jefeDeGrupo=datos['jefeDeGrupo'])
    def json(self):
        proyectoSchema = GrupoDeTrabajoSchema()
        return proyectoSchema.dump(self)
  
class StockSchema(Schema):
    lote = fields.Integer()
    detalleUbicacion = fields.String()
    unidad = fields.Integer()
    fechaVencimiento = fields.DateTime()
    id_espacioFisico = fields.Integer()
    codigoContenedor =  fields.String()

class GrupoDeTrabajoSchema(Schema):
    idProyecto = fields.Integer()
    nombre = fields.Str()
    jefeDeGrupo = fields.Integer(required=True,
    error_messages={"required": {"message": "Debe indicarse Jefe de Grupo", "code": 400}}
    ) 
    integrantes = fields.List(fields.Int())
    stock = fields.Nested(StockSchema, many=True)

    @post_load
    def make_Grupo(self, data, **kwargs):
        return GrupoDeTrabajo(**data)
  

