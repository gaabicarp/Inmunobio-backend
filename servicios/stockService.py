from marshmallow import ValidationError,EXCLUDE
from models.mongo.stock import Stock
from schemas.stockSchema import NuevoStockSchema,ModificarProducto,ConsumirStockSchema,StockSchema
from schemas.productosEnStockSchema import NuevoProductoEnStockSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.productoService import ProductoService
from exceptions.exception import ErrorProductoEnStockInexistente,ErrorStockInexistente,ErrorUnidadStock,ErrorStockVacio
from servicios.commonService import CommonService
from servicios.productosEnStockService import ProductoEnStockService

class StockService():
    @classmethod
    def nuevoStock(cls,datos):
        NuevoStockSchema().load(datos)
        cls.validarStock(datos['id_grupoDeTrabajo'],datos['id_espacioFisico'])
        productoEnSistema = ProductoService.find_by_id(datos['id_producto']) 
        cls.altaStock(datos,productoEnSistema)

    @classmethod
    def validarStock(cls,id_grupoDeTrabajo,id_espacioFisico):
        from servicios.espacioFisicoService import EspacioFisicoService
        GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)
        EspacioFisicoService.find_by_id(id_espacioFisico)

    @classmethod
    def altaStock(cls,datos,productoEnSistema):
        try:
            stock = cls.BusquedaEnStockAlta(datos['id_grupoDeTrabajo'],datos['id_espacioFisico'],datos['id_producto'])
            cls.altaProductoEnStock(stock,datos,productoEnSistema)
        except ErrorProductoEnStockInexistente :
            cls.crearStock(datos,productoEnSistema)

    def BusquedaEnStockAlta(_id_grupoDeTrabajo,_id_espacioFisico,_id_producto):
        resultado =  Stock.objects.filter(id_producto=_id_producto,id_espacioFisico = _id_espacioFisico, id_grupoDeTrabajo =_id_grupoDeTrabajo).first()
        if(not resultado):
            raise ErrorProductoEnStockInexistente(_id_producto)
        return resultado

    def BusquedaEnStock(_id_grupoDeTrabajo,_id_espacioFisico):
        return  Stock.objects.filter(id_espacioFisico = _id_espacioFisico, id_grupoDeTrabajo =_id_grupoDeTrabajo )
    
    def busquedaProductoPorAtributo(stock,productoNuevo):
        for producto in stock:
            if(ProductoEnStockService().compararProductos(producto,productoNuevo)): return producto
        return None
    @classmethod
    def BusquedaStockPorId(cls,_id_productoEnStock):
        resultado =  Stock.objects.filter(id_productoEnStock =_id_productoEnStock).first()
        if(not resultado):
            raise ErrorStockInexistente()
        return resultado

    def obtenerProductosEspecificos(_id_productos,productos):
        for prod in productos:
            if prod.id_productos == _id_productos: return prod
        raise ErrorProductoEnStockInexistente(_id_productos)

    @classmethod
    def crearProducto(cls,datos, productoEnSistema):
        productoNuevo = NuevoProductoEnStockSchema().load(datos,unknown=EXCLUDE )
        cls.setearUnidadesDeAgrupacion(productoEnSistema,productoNuevo)
        return productoNuevo

    @classmethod
    def altaProductoEnStock(cls,stock,datos,productoEnSistema):
        productoNuevo = cls.crearProducto(datos['producto'][0],productoEnSistema)
        productoEnStock = cls.busquedaProductoPorAtributo(stock.producto,productoNuevo)
        if not productoEnStock:
            stock.producto.append(productoNuevo)
        else:
            cls.modificarUnidades(productoEnStock.unidad + productoNuevo.unidad,productoEnStock)
        stock.save()

    @classmethod
    def modificarUnidades(cls,unidad,producto):
        if(unidad < 0 ):raise ErrorUnidadStock()
        if not unidad : raise ErrorStockVacio()    
        producto.unidad= unidad

    @classmethod
    def setearUnidadesDeAgrupacion(cls, productoSistema , producto):
        cls.modificarUnidades(producto.unidad * productoSistema.unidadAgrupacion,producto)

    @classmethod
    def crearStock(cls,datos,productoEnSistema):
        nuevoStock = NuevoStockSchema().load(datos,unknown=EXCLUDE)
        nuevoStock.nombre = productoEnSistema.nombre
        cls.setearUnidadesDeAgrupacion(productoEnSistema,nuevoStock.producto[0])
        nuevoStock.save()

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo,id_espacioFisico):
        cls.validarStock(id_grupoDeTrabajo,id_espacioFisico)
        stocks = StockSchema().dump(cls.BusquedaEnStock(id_grupoDeTrabajo,id_espacioFisico),many=True)       
        for stock in stocks:  
            for producto in stock['producto']:CommonService.asignarNombreContenedor(producto)
        return stocks


    @classmethod
    def borrarProductoEnStock(cls,id_productoEnStock,id_productos):
        stock= cls.BusquedaStockPorId(id_productoEnStock)
        productoEnStock = cls.obtenerProductosEspecificos(id_productos,stock.producto)
        stock.producto.remove(productoEnStock)
        cls.borradoStockVacio(stock)
        stock.save()
  
    @classmethod    
    def modificarProductoEnStock(cls,datos):
            ModificarProducto().load(datos)
            stock= cls.BusquedaStockPorId(datos['id_productoEnStock'])
            producto = cls.obtenerProductosEspecificos(datos['producto']['id_productos'],stock.producto)
            CommonService.updateAtributes(producto,datos['producto'],'unidad')
            stock.save()

    @classmethod
    def consumirStock(cls,datos):
        try:
            ConsumirStockSchema().load(datos)
            stock= cls.BusquedaStockPorId(datos['id_productoEnStock'])
            producto = cls.obtenerProductosEspecificos(datos['id_productos'],stock.producto)
            cls.modificarUnidades(producto.unidad - datos['unidad'],producto)
            stock.save()
        except ErrorStockVacio:
            stock.producto.remove(producto)
            stock.save()
            cls.borradoStockVacio(stock)
            
    @classmethod
    def borradoStockVacio(cls,stock):
        if(not stock.producto): stock.delete()
        stock.save()

    def borrarTodo(_id_grupoDeTrabajo):
        Stock.objects.filter(id_grupoDeTrabajo = _id_grupoDeTrabajo).delete()
        return {'Status':'ok'},200


