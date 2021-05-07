from db import dbMongo
from marshmallow import Schema, fields, post_load
import datetime
from dateutil import parser
class MuestraPropia(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.IntegerField()
    codigo = dbMongo.StringField()
    nombre = dbMongo.StringField()
    fecha = dbMongo.dateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
class FuenteExperimentalPropia(dbMongo.EmbeddedDocument):
    id_fuenteExperimental = dbMongo.IntegerField()
    especie = StringField()
    sexo = StringField()
    cepa = StringField()
    tipo = StringField()
    descripcion = StringField()
class GrupoExperimental(dbMongo.Document):
    id_grupoExperimental = dbMongo.SequenceField()
    id_experimento = dbMongo.intField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    tipo = dbMongo.StringField()
    fuentesExperimentales = dbMongo.ListField(dbMongo.EmbeddedDocumentField(FuenteExperimentalPropia))
    muestras = dbMongo.ListField(dbMongo.EmbeddedDocumentField(MuestraPropia)) #Guardar muestra propias (copia)
    parent = IntegerField(default = 0)
    habilitado = BooleanField(default = False)

    def json(self):
        return GrupoExperimentalSchema().dump(self)

class MuestraPropiaSchema(Schema):
    id_muestra = fields.Int()
    codigo = fields.Str()
    nombre = fields.Str()
    fecha = fields.DateTime()
    tipo = fields.Str()

class FuenteExperimentalPropiaSchema(Schema):
    id_fuenteExperimental = fields.Int()
    especie = fields.Str()
    sexo = fields.Str()
    cepa = fields.Str())
    tipo = fields.Str()
    descripcion = fields.Str()
class GrupoExperimentalSchema(Schema):
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    tipo = fields.Str()
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaSchema, many=True)
    muestras = fields.Nested(FuenteExperimentalPropiaSchema, many=True) #Guardar muestra propias (copia)
    parent = fields.Int()
    habilitado = fields.Bool()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return GrupoExperimental(**data)