from db import dbMongo

class Experimento(Document):
    id_experimiento = SequenceField()
    fechaInicio = DateTimeField(default=parser.parse(str(datetime.datetime.utcnow())))
    fechaFin = DateTimeField()
    resultados = SequenceField()
    finalizado = booleanField(default=False)
    metodologia = StringField()
    conclusiones = SequenceField()
    objetivos = StringField()
    gruposExperimentales = IntegerListField()