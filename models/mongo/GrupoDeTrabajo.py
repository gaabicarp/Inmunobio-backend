from db import dbMongo

class GrupoDeTrabajo(dbMongo.Document):
    nombre = StringField()
    jefeDeGrupo = IntField()
    integrantes = ListField()

    def toJson(self):
        return json.dumps(self)

