from models.mongo.producto import Producto
from schemas.productoSchema import ProductoSchema,NuevoProductoSchema,ModificarProductoSchema
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
            if(producto.detallesTecnicos):
                FileService.deleteFile(producto.detallesTecnicos)
            filename = FileService.upload(producto,archivo)
            producto.update(set__detallesTecnicos = filename)
            producto.reload()
 
    def validacionAltaProducto(id_distribuidora):
        DistribuidoraService().find_by_id(id_distribuidora)

    @classmethod
    def find_by_id(cls,id):
        producto =  Producto.objects(id_producto = id).first()
        if(not producto):
            raise Exception( f"No hay productos relacionados con id_producto: {id}")
        return producto     

    @classmethod
    def find_by_idDistribuidora(cls,_id_distribuidora):
        return Producto.objects(id_distribuidora = _id_distribuidora).all()
       
    @classmethod
    def bajaProducto(cls,id_producto):
        producto = cls.find_by_id(id_producto)
        cls.bajaProductoStockExterno([id_producto])
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
        producto = cls.find_by_id(id_producto)
        return CommonService.asignacionNombresDistribuidora(ProductoSchema().dump(producto))

    @classmethod
    def bajaStockExterno(cls,_id_distribuidora):
        cls.bajaProductoStockExterno(list(map(cls.obtenerIdProducto,cls.find_by_idDistribuidora(_id_distribuidora))))
        cls.borrarProductosDistribuidora(_id_distribuidora)
    
    @classmethod
    def borrarProductosDistribuidora(cls,_id_distribuidora):
        Producto.objects(id_distribuidora = _id_distribuidora).delete()

    @classmethod
    def obtenerIdProducto(cls,producto):
        return producto.id_producto

    @classmethod
    def obtenerNombreProducto(cls,id):
        return cls.find_by_id(id).nombre

    @classmethod
    def bajaProductoStockExterno(cls,idProductos):
        from servicios.stockService import StockService
        StockService.bajaExterna(idProductos)
    
    @classmethod
    def getGruposByProducto(cls,id_producto):
            from servicios.stockService import StockService
            return(list(map(cls.obtenerIdGrupo,StockService.stockContieneProducto(id_producto))))

    def obtenerIdGrupo(stock):
        from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
        return GrupoDeTrabajoService.find_by_id(stock['id_grupoDeTrabajo'])

