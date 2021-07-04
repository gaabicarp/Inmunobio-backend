from db import dbMongo

class Contenedor(dbMongo.Document):
    id_contenedor = dbMongo.SequenceField()
    codigo = dbMongo.StringField()
    nombre = dbMongo.StringField()
    descripcion = dbMongo.StringField()
    temperatura = dbMongo.StringField()
    id_proyecto = dbMongo.IntField()
    #La capacidad la manejan ellos.
    capacidad = dbMongo.IntField()
    fichaTecnica = dbMongo.StringField()
    disponible = dbMongo.BooleanField(default=True)
    parent = dbMongo.IntField(default = 0)
    id_espacioFisico = dbMongo.IntField()

