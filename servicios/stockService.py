#from dateutil import parser
#import datetime
from marshmallow import ValidationError,EXCLUDE
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema
from schemas.productosSchema import NuevoProductosSchema, ProductosSchema
from schemas.productoEnStockSchema import NuevoProductoEnStockSchema
from schemas.grupoTrabajoSchema import GrupoDeTrabajoSchema, NuevoStockGrupoSchema,busquedaStocksSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.productoService import ProductoService
from exceptions.exception import ErrorGrupoInexistente,ErrorProductoInexistente,ErrorStockEspacioFisicoInexistente
from models.mongo.grupoDeTrabajo import GrupoDeTrabajo
from servicios.commonService import CommonService

class StockService():
    @classmethod
    def nuevoStock(cls,datos):
        try:
            NuevoStockGrupoSchema().load(datos)
            cls.validarNuevoStock(datos)
            grupo = cls.obtenerGrupo(datos)
            return cls.altaStock(grupo, datos)
        except ValidationError as err:
            return {'error': err.messages},400
            #ver como anidar estos dos errores 
        except ErrorGrupoInexistente as err:
            return {'error':err.message},400
        except ErrorProductoInexistente as err:
            return {'error':err.message},400

    @classmethod
    def validarNuevoStock(cls,datos):
        #ver si espacio fisico queindifcan existe
        cls.obtenerProducto(datos['stock']['productos'][0])
        #buscar y devolver es correcto? preguntar
        cls.obtenerGrupo(datos)

    @classmethod
    def obtenerProducto(cls,datos):
        return ProductoService.find_by_id(datos['id_producto']) 

    @classmethod
    def obtenerGrupo(cls,datos):
        return GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo']) #and producto existe en sistema

    def criterioBusquedaStock(stock,stockNuevo):
        return stock.id_espacioFisico == stockNuevo['id_espacioFisico']   

    def criterioBusquedaProductoEnStock(producto,productoNuevo):
        return producto.id_producto == productoNuevo['id_producto'] 

    def criterioBusquedaProductos(producto,productoNuevo):
        for key,value in productoNuevo.items():
            if hasattr(producto, key)and getattr(producto,key)!= value:return False
        return True

    def filtrarPorEspacioFisico(stock,_id_espacioFisico):
        return stock.id_espacioFisico == _id_espacioFisico
    def filtrarPorIdProducto(producto,_id_producto):

        return producto.id_productoEnStock == _id_producto
    def filtrarPorIdProductos(productos,_id_productos):
        return productos.id_productos == _id_productos

    @classmethod
    def busquedaEnStock(cls,objetos,datos,criterioBusqueda):
        resultado = list(filter(lambda x: criterioBusqueda(x,datos) , objetos))
        if (not len(resultado)): return resultado
        return resultado[0]

    @classmethod
    def altaStock(cls,grupoTrabajo,datos):
        stockProducto = cls.busquedaEnStock(grupoTrabajo.stock,datos['stock'],cls.criterioBusquedaStock)
        if(not stockProducto):
            #creo el stock que corresponde a ese EspacioFisico
            cls.crearStock(datos,grupoTrabajo) 
        else:
            cls.modificarStockExistente(stockProducto,datos['stock']['productos'][0])
        grupoTrabajo.save()
        return {'Status':'ok'},200 
    
    @classmethod
    def modificarStockExistente(cls,stockExistente,nuevoProducto):
        productoEnStock = cls.busquedaEnStock(stockExistente.productos,nuevoProducto,cls.criterioBusquedaProductoEnStock) 
        if(not productoEnStock):
            cls.crearProductoEnStock(stockExistente,nuevoProducto)
        else:
            cls.modficarProductoExistente(productoEnStock,nuevoProducto)

    @classmethod
    def modficarProductoExistente(cls,productoEnStock,nuevoProducto):
        productos = cls.busquedaEnStock(productoEnStock.producto,nuevoProducto['producto'][0],cls.criterioBusquedaProductos) 
        if(not productos):
            return cls.crearProductos(productoEnStock,nuevoProducto['producto'][0])
        return cls.modificarUnidades(productos,productos.unidad+nuevoProducto['producto'][0]['unidad'])

    @classmethod
    def modificarUnidades(cls,producto,unidad):
        producto.unidad= unidad
    
    @classmethod
    def crearStock(cls,datos,grupoTrabajo):
        nuevoStock = NuevoStockSchema().load(datos['stock'],unknown=EXCLUDE )
        grupoTrabajo.stock.append(nuevoStock)
        grupoTrabajo.save()
        return nuevoStock

    #deberia en service de producto en stock
    @classmethod
    def crearProductoEnStock(cls,stockExistente,datos):
        nuevoProductoEnStock=NuevoProductoEnStockSchema().load(datos,unknown=EXCLUDE)
        stockExistente.productos.append(nuevoProductoEnStock)


    def crearProductos(productoEnStock,nuevoProducto):
        nuevoProductos = NuevoProductosSchema().load(nuevoProducto,unknown=EXCLUDE )
        productoEnStock.producto.append(nuevoProductos)

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo,id_espacioFisico):
        try:
            GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo) #valido q exista grupo
            #faltabuscar espaciofisico y si no encuentra lanza excep
            stock =  cls.stockSegunEspacioFisico(id_grupoDeTrabajo,id_espacioFisico)
            return CommonService.json(stock,StockSchema)
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400
        except ErrorStockEspacioFisicoInexistente as err:
            return {'Error':err.message},400
 
    @classmethod
    def stockSegunEspacioFisico(cls,_id_grupoDeTrabajo,_id_espacioFisico):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=_id_grupoDeTrabajo,stock__id_espacioFisico= _id_espacioFisico).first()
        if (not grupo):
            raise ErrorStockEspacioFisicoInexistente()
        return cls.busquedaEnStock(grupo.stock,_id_espacioFisico,cls.filtrarPorEspacioFisico)
 
    @classmethod
    def obtenerStocks(cls,_id_grupoDeTrabajo):     
        return CommonService.jsonMany(GrupoDeTrabajoService.find_by_id(_id_grupoDeTrabajo).stock,StockSchema)

    @classmethod
    def borrarProductoEnStock(cls,datos):
        '''recibe un json con id grupo de trabajo, id de stock e id de producto en stock,
        si hay coincidencia lo borra'''
        try:
            busquedaStocksSchema().load(datos)
            grupo = cls.obtenerGrupo(datos)
            #grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=datos['id_grupoDeTrabajo'],stock__id_espacioFisico= datos['id_espacioFisico']).first()
            stock = cls.busquedaEnStock(grupo.stock,datos['id_espacioFisico'],cls.filtrarPorEspacioFisico)
            #print('stock egun espacio fisico:', stock)
            stockDeProducto = cls.busquedaEnStock(stock.productos,datos['id_productoEnStock'],cls.filtrarPorIdProducto)
            producto = cls.busquedaEnStock(stockDeProducto.producto,datos['id_productos'],cls.filtrarPorIdProductos)
            stockDeProducto.producto.remove(producto)

            grupo.save()
            return {'Status':'ok'},200 
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400
        except ErrorStockEspacioFisicoInexistente as err:
            return {'Error':err.message},400            


        



