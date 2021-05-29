from db import dbMongo
from marshmallow import Schema, fields, post_load
import datetime
from dateutil import parser
class MuestraPropia(dbMongo.EmbeddedDocument):
    id_muestra = dbMongo.IntField()
    codigo = dbMongo.StringField()
    nombre = dbMongo.StringField()
    fecha = dbMongo.DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    tipo = dbMongo.StringField()
class FuenteExperimentalPropia(dbMongo.EmbeddedDocument):
    id_fuenteExperimental = dbMongo.SequenceField()
    codigo = dbMongo.StringField(default="")
    codigoGrupoExperimental = dbMongo.StringField()
    especie = dbMongo.StringField()
    sexo = dbMongo.StringField()
    cepa = dbMongo.StringField()
    tipo = dbMongo.StringField()
    descripcion = dbMongo.StringField()

class GrupoExperimental(dbMongo.Document):
    id_grupoExperimental = dbMongo.SequenceField()
    id_experimento = dbMongo.IntField()
    codigo = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    tipo = dbMongo.StringField()
    fuentesExperimentales = dbMongo.ListField(dbMongo.EmbeddedDocumentField(FuenteExperimentalPropia))
    muestras = dbMongo.ListField(dbMongo.EmbeddedDocumentField(MuestraPropia)) #Guardar muestra propias (copia)
    parent = dbMongo.IntField(default = 0)
    habilitado = dbMongo.BooleanField(default = True)

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
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    especie = fields.Str()
    sexo = fields.Str()
    cepa = fields.Str()
    tipo = fields.Str()
    descripcion = fields.Str()
class GrupoExperimentalSchema(Schema):
    id_grupoExperimental = fields.Int()
    id_experimento = fields.Int()
    codigo = fields.Str()
    descripcion = fields.Str()
    tipo = fields.Str()
    fuentesExperimentales = fields.Nested(FuenteExperimentalPropiaSchema, many=True)
    muestras = fields.Nested(MuestraPropiaSchema, many=True) #Guardar muestra propias (copia)
    parent = fields.Int()
    habilitado = fields.Bool()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return GrupoExperimental(**data)

class AltaGrupoExperimentalSchema(GrupoExperimentalSchema):
    id_experimento = fields.Int(required=True, error_messages={"required": {"message" : "Es necesario indicar el id del experimento", "code": 400}})
    codigo = fields.Str( required=True, error_messages={"required": {"message": "Es necesario indicar el codigo del grupo experimental", "code": 400}})
    tipo = fields.Str(required=True, error_messages={"required": {"message": "Es necesario indicar el tipo del grupo experimental", "code": 400}})

