from marshmallow import ValidationError
from flask import jsonify
from models.mongo.producto import Producto
from schemas.productoSchema import ProductoSchema,NuevoProductoSchema,IdProductoSchema,modificarProductoSchema
from exceptions.exception import ErrorProductoInexistente,ErrorDistribuidoraInexistente
from servicios.commonService import CommonService
from servicios.distribuidoraService import DistribuidoraService
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
        except ErrorDistribuidoraInexistente as err:
            return {'error': err.message},400


    def validacionAltaProducto(id_distribuidora):
        #valida que exista la distribuidora y qué mas??
        DistribuidoraService().find_by_id(id_distribuidora)
        

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

    def json(datos):
        return ProductoSchema().dump(datos)

    def jsonMany(datos):
        return jsonify(ProductoSchema().dump(datos,many=True))

    @classmethod
    def obtenerProductos(cls):
        return cls.jsonMany(Producto.objects().all())

    @classmethod
    def modificarProducto(cls,datos):
        try:
            modificarProductoSchema().load(datos)
            producto = cls.find_by_id(datos['id_producto'])
            CommonService.updateAtributes(producto,datos)
            producto.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400

    @classmethod        
    def obtenerProducto(cls,id_producto):
        try:
            producto = cls.find_by_id(id_producto)
            return cls.json(producto)
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400
        

         
