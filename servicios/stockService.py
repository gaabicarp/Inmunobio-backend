from marshmallow import EXCLUDE
from models.mongo.stock import Stock
from schemas.stockSchema import NuevoStockSchema,ModificarProducto,ConsumirStockSchema,StockSchema
from servicios.productoService import ProductoService
from servicios.commonService import CommonService
from servicios.productosEnStockService import ProductoEnStockService

class StockService():
    @classmethod
    def validarStock(cls,id_grupoDeTrabajo,id_espacioFisico):
        from servicios.espacioFisicoService import EspacioFisicoService
        EspacioFisicoService.find_by_id(id_espacioFisico)
        from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
        GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)

    @classmethod
    def validarStockNuevo(cls,datos):
        cls.validarStock(datos['id_grupoDeTrabajo'] ,datos['id_espacioFisico'])
        cls.validarStockContendor(datos)

    @classmethod
    def validarStockContendor(cls,datos):   
        from servicios.contenedorService import ContenedorService
        contenedor = ContenedorService.find_by_id(datos['producto']['codigoContenedor'])
        if contenedor.id_espacioFisico != datos['id_espacioFisico']: raise Exception('El contenedor no pertenece al espacio fisico indicado')

    @classmethod
    def nuevoStock(cls,datos):
        stockNuevo = NuevoStockSchema().load(datos)
        cls.validarStockNuevo(datos)
        cls.altaStock(stockNuevo,ProductoService.find_by_id(stockNuevo.id_producto))

    @classmethod
    def altaStock(cls,stockNuevo,productoEnSistema):
        stockExistente = cls.busquedaStockExistente(stockNuevo)
        if stockExistente:
            cls.altaProductoEnStock(stockExistente,stockNuevo,productoEnSistema)
        else: cls.crearStock(stockNuevo,productoEnSistema)

    def busquedaStockExistente(stockNuevo):
        return Stock.objects.filter(id_producto=stockNuevo.id_producto,id_espacioFisico = stockNuevo.id_espacioFisico, id_grupoDeTrabajo =stockNuevo.id_grupoDeTrabajo).first()

    def BusquedaEnStock(_id_grupoDeTrabajo,_id_espacioFisico):
        return  Stock.objects.filter(id_espacioFisico = _id_espacioFisico, id_grupoDeTrabajo =_id_grupoDeTrabajo )
    
    def busquedaProductoPorAtributo(stock,productoNuevo):
        for producto in stock:
            if(ProductoEnStockService().compararProductos(producto,productoNuevo)): return producto

    @classmethod
    def modificarUnidades(cls,unidad,producto):
        cls.validarUnidadesStock(unidad)
        producto.unidad= unidad
    
    @classmethod
    def validarUnidadesStock(cls,unidad):
        if unidad < 0 : raise Exception("Las unidades de Stock deben ser numeros enteros positivos / la consumicion de stock no debe pasar del total de unidades")    

    @classmethod
    def altaProductoEnStock(cls,stockExistente,stockNuevo,productoEnSistema):
        productoNuevo = stockNuevo.producto
        cls.setearUnidadesDeAgrupacion(productoEnSistema,productoNuevo)
        productoEnStock = cls.busquedaProductoPorAtributo(stockExistente.producto,productoNuevo)
        if productoEnStock:
            cls.modificarUnidades(productoEnStock.unidad + productoNuevo.unidad,productoEnStock)
        else:
            stockExistente.producto.append(productoNuevo)
        stockExistente.save()

    @classmethod
    def setearUnidadesDeAgrupacion(cls, productoSistema , producto):
        cls.modificarUnidades(producto.unidad * productoSistema.unidadAgrupacion,producto)

    @classmethod
    def crearStock(cls,nuevoStock,productoEnSistema):
        nuevoStock.producto = [cls.setearNuevoProducto(nuevoStock,nuevoStock.producto,productoEnSistema)]
        nuevoStock.save()

    @classmethod
    def setearNuevoProducto(cls,nuevoStock,nuevoProducto,productoEnSistema):
        nuevoProducto =  nuevoStock.producto
        nuevoProducto.nombre = productoEnSistema.nombre
        cls.setearUnidadesDeAgrupacion(productoEnSistema,nuevoProducto)
        return nuevoProducto

    @classmethod
    def BusquedaStockPorId(cls,_id_productoEnStock):
        stock =  Stock.objects.filter(id_productoEnStock =_id_productoEnStock).first()
        if not stock : raise Exception(f"No existe stock asociado con id_productoEnStock {id}")
        return stock

    def obtenerProductosEspecificos(_id_productos,productos):
        for prod in productos: 
            if prod.id_productos == _id_productos: return prod
        raise Exception(f"No hay productos activos con id_productos {_id_productos}")

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo,id_espacioFisico):
        cls.validarStock(id_grupoDeTrabajo,id_espacioFisico)
        stocks = StockSchema().dump(cls.BusquedaEnStock(id_grupoDeTrabajo,id_espacioFisico),many=True)       
        for stock in stocks:  cls.asignarDatosExtraStock(stock)
        return stocks
    
    @classmethod
    def asignarDatosExtraStock(cls,stock):
        CommonService.asignarNombreProducto(stock)
        for producto in stock['producto']: CommonService.asignarNombreContenedor(producto)

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
        ConsumirStockSchema().load(datos)
        stock= cls.BusquedaStockPorId(datos['id_productoEnStock'])
        producto = cls.obtenerProductosEspecificos(datos['id_productos'],stock.producto)
        cls.modificarUnidades(producto.unidad - datos['unidad'],producto)
        stock.save()
        cls.borradoProductoEnStock(stock,producto)

    @classmethod
    def borradoProductoEnStock(cls,stock,producto):
        if not producto.unidad :
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

    @classmethod
    def bajaExterna(cls,idsProducto):
        for id in idsProducto : cls.bajaProductoExterno(id)
    
    @classmethod 
    def bajaProductoExterno(cls,idProducto):
        return Stock.objects(id_producto = idProducto).delete()
    
    @classmethod
    def stockContieneProducto(cls,idProducto):
        stocks = Stock.objects(id_producto = idProducto)
        return StockSchema().dump(stocks,many=True)       


