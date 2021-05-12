from marshmallow import ValidationError,EXCLUDE
from flask import jsonify, request
from models.mongo.producto import Producto
from schemas.productoSchema import ProductoSchema,NuevoProductoSchema,IdProductoSchema

from exceptions.exception import ErrorProductoInexistente
class ProductoService():

    @classmethod
    def altaProducto(cls,datos):
        try:
            nuevoProducto = NuevoProductoSchema().load(datos)
            if(cls.validacionProducto()):
                nuevoProducto.save()
                return {'Status':'ok'},200
            return  {'error':'Datos incorrectos '},400
        except ValidationError as err:
            return {'error': err.messages},400

    def validacionProducto():
        return True

    def find_by_id(id):
        producto =  Producto.objects(id_producto = id)
        if(not producto):
            raise ErrorProductoInexistente()
        return producto     

    @classmethod
    def bajaProducto(cls,datos):
        try:
            IdProductoSchema().load(datos)
            producto = cls.find_by_id(datos['id_producto'])
            producto.remove()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400

 