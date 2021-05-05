from marshmallow import Schema, fields, post_load, ValidationError
from db import dbMongo

class Producto(Document):
    nombre = StringField()
    tipo = StringField()
    aka = StringField()
    marca = StringField()
    url = StringField()
    unidadAgrupacion = StringField()
    detallesTecnicos = StringField() #Se sube archivo .txt
    protocolo = StringField() #Se sube archivo
    id_distribuidora = ReferenciasField(required=True)
    id_producto = SequenceField()
