from db import dbMongo
"""
class Blog(EmbeddedDocument):
    fecha = DateTimeField()
    detalle = StringField()
    id_usuario = IntField()

 class Stock(EmbeddedDocument):
    lote = StringField()#Charlar stock y lote
    detalleUbicacion = StringField()
    unidad = IntField()
    fechaVencimiento = DateTimeField()
    id_espacioFisico = ReferenciasField(EspacioFisico, required=True)
    codigoContenedor = StringField() 

class GrupoDeTrabajo(Document):
    nombre = StringField()
    jefeDeGrupo = IntField()
    integrantes = ListField()
    stock = EmbeddedDocumentListField('Stock') 

class Herramienta(EmbeddedDocument):
    nombre = StringField()
    detalle_protocolo = StringField()
    blogs = EmbeddedDocumentListField('Blog')

class Animal(EmbeddedDocument):
    codigo = StringField()
    especie = StringField()
    cepa = StringField()
    sexo = StringField()

class TipoDeJaula(Document):
    codigo = StringField()
    capacidad = IntField()
    nombre = StringField()

class Jaula(EmbeddedDocument):
    codigo = StringField()
    nombre = StringField()
    numero = IntField()
    rack = IntField()
    estante = IntField()
    tipo = ReferenciasField(TipoDeJaula, required=True)#Consultar
    animales = EmbeddedDocumentListField('Animal')
    blogs = EmbeddedDocumentListField('Blog')

class EspacioFisico(Document):
    nombre = StringField()
    piso = StringField()
    sala = StringField()
    descripcion = StringField()
    blogs = EmbeddedDocumentListField('Blog')
    tipo = StringField() #Revisar y preguntar /Taller, Bioterio, etc
    herramientas = EmbeddedDocumentListField('Herramienta')
    jaulas = EmbeddedDocumentListField('Jaula')

class subContenedores(EmbeddedDocument):
    codigo = StringField()
    fichaTecnica = StringField()
    descripcion = StringField()
    Nombre = StringField()
    temperatura = StringField()
    subContenedores = EmbeddedDocumentListField('subContenedores')
class Contenedor(Document):
    codigo = StringField()
    fichaTecnica = StringField()
    descripcion = StringField()
    Nombre = StringField()
    temperatura = StringField()
    id_espacioFisico = ReferenciasField(EspacioFisico, required=True)
    contenedores = EmbeddedDocumentListField('Contenedores')
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
    id_producto-> agregar

class Productob(embebido):
    nombre
    id_producto <- id_producto
    unidad = dbMongo.IntField()
class Distribuidora(Document):
    nombre = StringField()
    direccion = StringField()
    contacto = StringField()
    cuit = StringField()
    representante = StringField()

class GrupoExperimental(EmbeddedDocument):
    codigo = StringField()
    descripcion = StringField()

class FuenteExperimental(Document):
    cepa = StringField() #lo ponemos solo en animal?
    tipo = StringField() #Animal u otros
    descripcion = StringField()
    animal = EmbeddedDocument("Animal") #?
    gruposExperimentales = EmbeddedDocumentListField('GrupoExperimental')

class FuenteExperimental(EmbeddedDocument):
    cepa = StringField() #lo ponemos solo en animal?
    tipo = StringField() #Animal u otros
    animal = EmbeddedDocument('Animal')
    descripcion = StringField()

class Muestra(EmbeddedDocument):
    nombre = StringField()
    fecha = DateTimeField()
    tipo = StringField()
class GrupoExperimental(EmbeddedDocument):
    fuentesExperimentales = EmbeddedDocumentListField('FuenteExperimental')
    muestas = EmbeddedDocumentListField('Muestra')
    descripcion = StringField()
class Experimento(Document):
    gruposExperimentales = EmbeddedDocumentListField('GrupoExperimental')
"""