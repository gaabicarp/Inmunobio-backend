from db import dbMongo

class FuenteExperimental(dbMongo.Document):
    id_fuenteExperimental = dbMongo.SequenceField()
    codigo = dbMongo.StringField(default="")
    codigoGrupoExperimental = dbMongo.StringField() #Se usa como flag para saber si está disponible
    especie = dbMongo.StringField()
    sexo = dbMongo.StringField()
    cepa = dbMongo.StringField()
    tipo = dbMongo.StringField()
    descripcion = dbMongo.StringField()

    def json(self):
        return FuenteExperimentalSchema().dump(self)

class FuenteExperimentalSchema(dbMongo.EmbeddedDocument):
    id_fuenteExperimental = fields.Int()
    codigo = fields.Str()
    codigoGrupoExperimental = fields.Str()
    especie = fields.Str()
    sexo = fields.Str()
    cepa = fields.Str()
    tipo = fields.Str()
    descripcion = fields.Str()

    @post_load
    def make_Proyecto(self, data, **kwargs):
        return FuenteExperimental(**data)