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
            #aca devuelve el id del producto para luego pasarselo a l subida del archivo
            #y guardar el archivo con esa id
            nuevoProducto = NuevoProductoSchema().load(datos)
            cls.validacionAltaProducto(datos['id_distribuidora'])
            nuevoProducto.save()
            return nuevoProducto.id_producto
       

    @classmethod
    def asociarArchivo(cls,archivo,_id_producto):
            producto = cls.find_by_id(_id_producto)
            filename = FileService.upload(archivo)
            if(producto.detallesTecnicos):
                FileService.deleteFile(producto.detallesTecnicos)
            producto.update(set__detallesTecnicos = filename)
            producto.reload() 
 
    def validacionAltaProducto(id_distribuidora):
        #valida que exista la distribuidora y qué mas??
        DistribuidoraService().find_by_id(id_distribuidora)

    @classmethod
    def find_by_id(cls,id):
        producto =  Producto.objects(id_producto = id).first()
        if(not producto):
            raise ErrorProductoInexistente(id)
        return producto     
    @classmethod
    def find_by_id(cls,id):
        producto =  Producto.objects(id_producto = id).first()
        if(not producto):
            raise ErrorProductoInexistente(id)
        return producto 

    @classmethod
    def find_by_idDistribuidora(cls,_id_distribuidora):
        productos =  Producto.objects(id_distribuidora = _id_distribuidora).all()
        if(not productos):
            #raise ErrorProductoInexistente(id) -> Ver
            print("No hay productos con id distribuidora")
        return productos 

    @classmethod
    def bajaProducto(cls,id_producto):
            producto = cls.find_by_id(id_producto)
            producto.delete()
   
    @classmethod
    def obtenerProductos(cls):
        productos = ProductoSchema().dump(Producto.objects(),many=True)
        for producto in productos : CommonService.asignacionNombresDistribuidora(producto)
        return productos

    @classmethod
    def modificarProducto(cls,datos):
            ModificarProductoSchema().load(datos)
            producto = cls.find_by_id(datos['id_producto'])
            CommonService.updateAtributes(producto,datos,'id_producto')
            producto.save()

    def obtenerProducto(cls,id_producto):
        try:
            producto = cls.find_by_id(id_producto)
            return CommonService.asignacionNombresDistribuidora(ProductoSchema().dump(producto),producto.id_distribuidora)
        except ErrorProductoInexistente as err:
            return {'Error': err.message},400
        
    @classmethod
    def bajaDistribuidora(cls,_id_distribuidora):
        print('Entro a baja de producto')
        from servicios.stockService import StockService
        StockService.bajaDistribuidora(list(map(cls.obtenerIdProducto,cls.find_by_idDistribuidora(_id_distribuidora))))
        cls.borrarProductosDistribuidora(_id_distribuidora)
    
    @classmethod
    def borrarProductosDistribuidora(cls,_id_distribuidora):
        Producto.objects(id_distribuidora = _id_distribuidora).delete()

    @classmethod
    def obtenerIdProducto(cls,producto):
        return producto.id_producto

