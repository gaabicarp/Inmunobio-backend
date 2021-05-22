from marshmallow import ValidationError
from models.mongo.producto import Producto
from schemas.productoSchema import ProductoSchema,NuevoProductoSchema,IdProductoSchema,ModificarProductoSchema
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
        producto =  Producto.objects(id_producto = id).first()
        if(not producto):
            raise ErrorProductoInexistente(id)
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


    @classmethod
    def obtenerProductos(cls):
        return CommonService.jsonMany(Producto.objects(),ProductoSchema)

    @classmethod
    def modificarProducto(cls,datos):
        try:
            ModificarProductoSchema().load(datos)
            producto = cls.find_by_id(datos['id_producto'])
            CommonService.updateAtributes(producto,datos,'id_producto')
            producto.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400

    def obtenerProducto(cls,id_producto):
        try:
            producto = cls.find_by_id(id_producto)
            return CommonService.json(producto,ProductoSchema)
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400
        

         
