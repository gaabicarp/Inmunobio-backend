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
            cls.validacionAltaProducto(datos['id_distribuidora'])
            nuevoProducto.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400

    def validacionAltaProducto(id_distribuidora):
        #valida que exista la distribuidora
        #DistribuidoraService().find_by_id(id_distribuidora)
        pass

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
            producto.delete()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400
    
    def jsonMany(datos):
        return jsonify(ProductoSchema().dump(datos,many=True))

    @classmethod
    def obtenerProductos(cls):
        return cls.jsonMany(Producto.objects().all())
