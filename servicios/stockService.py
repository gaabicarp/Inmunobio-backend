#from dateutil import parser
#import datetime
from marshmallow import ValidationError,EXCLUDE
from flask import jsonify
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema
from schemas.productosSchema import NuevoProductosSchema
from schemas.productoEnStockSchema import NuevoProductoEnStockSchema
from schemas.grupoTrabajoSchema import NuevoStockGrupoSchema,busquedaStocksSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.productoService import ProductoService
from exceptions.exception import ErrorGrupoInexistente,ErrorProductoInexistente

class StockService():
    @classmethod
    def nuevoStock(cls,datos):
        try:
            NuevoStockGrupoSchema().load(datos)
            cls.validarNuevoStock(datos)
            return cls.altaStock(cls.obtenerGrupo(datos), datos)
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
            if (hasattr(producto, key) and (producto.key != value)): return False
        return True
    @classmethod
    def busquedaEnStock(cls,objetos,datos,criterioBusqueda):
        resultado = list(filter(lambda x: criterioBusqueda(x,datos) , objetos))
        if (not len(resultado)): return resultado
        return resultado[0]

    @classmethod
    def altaStock(cls,grupoTrabajo,datos):
        stockProducto = cls.busquedaEnStock(grupoTrabajo.stock,datos['stock'],cls.criterioBusquedaStock)
        if(not stockProducto):
            #antes de seguir creo el stock que corresponde a ese EspacioFisico
            stockProducto = cls.crearStock(datos,grupoTrabajo)      
        print(' modifico stock existente, hubo coincidencia con espacio fisico ')
        cls.modificarStockExistente(stockProducto,datos['stock']['productos'][0])
        grupoTrabajo.save()
        return {'Status':'ok'},200 
    
    @classmethod
    def modificarStockExistente(cls,stockExistente,nuevoProducto):
        productoEnStock = cls.busquedaEnStock(stockExistente.productos,nuevoProducto,cls.criterioBusquedaProductoEnStock) 
        if(not productoEnStock):
            print('no hubo coincidencia con id de producto, creo una nnueva instancia')
            productoEnStock = cls.crearProductoEnStock(stockExistente,nuevoProducto['productos'][0])
        print('hay coincidencia con id de producto')
        cls.modficarProductoExistente(productoEnStock,nuevoProducto)
   
    @classmethod
    def modficarProductoExistente(cls,productoEnStock,nuevoProducto):
        print(nuevoProducto)
        print('ESTOY EN MODIFICAR PRODUCTO EXISTENEEEEEEEEEEEEE')
        print(productoEnStock)
        productos = cls.busquedaEnStock(productoEnStock.producto,nuevoProducto,cls.criterioBusquedaProductos) 
        if(not productoEnStock):
            print('no hubo coincidencia con otros productos, creo una nueva instancia')
            productoEnStock = cls.crearProductos(productoEnStock,nuevoProducto)
        print('hay coincidencia con otros productos')
        #cls.modficarProductoExistente(productoEnStock,nuevoProducto)
        print(productos)
        cls.modificarUnidades(productoEnStock,productos.unidad+nuevoProducto['producto'][0]['unidad'])

    @classmethod
    def modificarUnidades(cls,producto,unidad):
        print('se encuentra stock con mismo lote y mismo id espacio fisico modif unidades')
        producto.unidad= unidad
    
    @classmethod
    def crearStock(cls,datos,grupoTrabajo):
        nuevoStock = NuevoStockSchema().load(datos['stock'],unknown=EXCLUDE )
        grupoTrabajo.stock.append(nuevoStock)
        #grupoTrabajo.save()
        return nuevoStock
    #deberia en service de producto en stock
    @classmethod
    def crearProductoEnStock(cls,stockExistente,datos):
        print(datos)
        nuevoProductoEnStock=NuevoProductoEnStockSchema().load(datos,unknown=EXCLUDE)
        stockExistente.producto.append(nuevoProductoEnStock)
        return nuevoProductoEnStock


    def crearProductos(productoEnStock,nuevoProducto):
        nuevoProductos = NuevoStockSchema().load(nuevoProducto,unknown=EXCLUDE )
        productoEnStock.productos.append(nuevoProductos)
        #grupoTrabajo.save()
        return nuevoProductos

    def jsonMany(datos):
        return jsonify(StockSchema().dump(datos,many=True))
    def json(datos):
        return StockSchema().dump(datos)

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo):
        try:
            grupo = GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)
            if (grupo):
                return cls.jsonMany(grupo.stock)
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400

    #def busquedaPorId():
    @classmethod
    def borrarProductoEnStock(cls,datos):
        '''recibe un json con id grupo de trabajo, id de stock e id de producto en stock,
        si hay coincidencia lo borra'''

        



