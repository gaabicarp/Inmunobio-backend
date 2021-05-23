from marshmallow import ValidationError
from models.mongo.producto import Producto
from schemas.productoSchema import ProductoSchema,NuevoProductoSchema,IdProductoSchema,ModificarProductoSchema
from exceptions.exception import ErrorProductoInexistente,ErrorDistribuidoraInexistente
from servicios.commonService import CommonService
from servicios.distribuidoraService import DistribuidoraService
from servicios.fileService import FileService

class ProductoService():

    @classmethod
    def altaProducto(cls,datos):
        try:
            #aca devuelve el id del producto para luego pasarselo a l subida del archivo
            #y guardar el archivo con esa id
            nuevoProducto = NuevoProductoSchema().load(datos)
            cls.validacionAltaProducto(datos['id_distribuidora'])
            nuevoProducto.save()
            print(nuevoProducto.id_producto)
            return {'Status':'ok','id_producto':nuevoProducto.id_producto},200
        except ValidationError as err:
            return {'Error': err.messages},400
        except ErrorDistribuidoraInexistente as err:
            return {'Error': err.message},400 

    def asociarArchivo(cls,archivo,_id_producto):
        filename = FileService.upload(archivo)

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
        

         
