from db import dbMongo
import datetime
from dateutil import parser
from models.mongo import blog

from marshmallow import Schema, fields, post_load, validate
from models.mongo.validacion import Validacion


class MuestraExterna(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.IntField()
    codigo = dbMongo.StringField()
    fecha = dbMongo.DateTimeField()
    tipo = dbMongo.StringField()
    id_proyecto = dbMongo.IntField()
    id_grupoExperimental = dbMongo.IntField()
    id_experimento = dbMongo.IntField()
    descripcion = dbMongo.StringField()
    id_contenedor= dbMongo.IntField()
    habilitada = dbMongo.BooleanField(default=True)

class MuestraExternaSchema(Schema):
    id_muestra = fields.Int()
    codigo = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()
    id_proyecto = fields.Int()
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    descripcion = fields.Str()
    id_contenedor = fields.Int()
    habilitada = fields.Boolean()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return MuestraExterna(**data)

class Experimento(dbMongo.Document):
    id_experimento = dbMongo.SequenceField()
    id_proyecto = dbMongo.IntField()
    codigo = dbMongo.StringField()
    fechaInicio = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFin = dbMongo.DateTimeField()
    resultados = dbMongo.StringField(default="")
    finalizado = dbMongo.BooleanField(default=False)
    metodologia = dbMongo.StringField()
    conclusiones = dbMongo.StringField(default="")
    objetivos = dbMongo.StringField()
    muestrasExternas = dbMongo.ListField(dbMongo.EmbeddedDocumentField('MuestraExterna'))
    blogs = dbMongo.ListField(dbMongo.EmbeddedDocumentField('Blog'))


    """     def json(self):
        return ().dump(self) """
    

