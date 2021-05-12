#from dateutil import parser
#import datetime
from marshmallow import ValidationError,EXCLUDE
from flask import jsonify, request
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema
from schemas.productoEnStockSchema import NuevoProductoEnStockSchema
from schemas.grupoTrabajoSchema import NuevoStockGrupoSchema,busquedaStocksSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService

class StockService():
    @classmethod
    def nuevoStock(cls,datos):
        try:
            NuevoStockGrupoSchema().load(datos)
            if(cls.validarNuevoStock(datos)):
                return cls.altaStock(cls.obtenerGrupo(datos), datos)
            return  {'error':'Grupo de trabajo inexistente'},400
        except ValidationError as err:
            return {'error': err.messages},400

    @classmethod
    def validarNuevoStock(cls,datos):
        return cls.obtenerProducto(datos) and cls.obtenerGrupo(datos)
        
    @classmethod
    def obtenerProducto(cls,datos):
        return True

    @classmethod
    def obtenerGrupo(cls,datos):
        return GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo']) #and producto existe en sistema

    @classmethod
    def altaStock(cls,grupoTrabajo,datos):
        stockProducto = cls.busquedaEnStock(grupoTrabajo.stock,datos['stock'])
        if(stockProducto):
            print(' modifico stock existente, hubo coincidencia con lote e id')
            cls.modificarStockExistente(stockProducto[0],datos['stock']['producto'][0])
        else:
           cls.crearStock(datos,grupoTrabajo)
        grupoTrabajo.save()
        return {'Status':'ok'},200 
  
    @classmethod
    def busquedaEnStock(cls,stocks,datos):
        '''Recibe lista con stocks y stock a dar de alta, devuelve un stock que coincida con id_producto
        a dar de alta,o [] si no encuentra'''
        return list(filter(lambda x: cls.criterioBusqueda(x,datos), stocks))
    
    def criterioBusqueda(stock,stockNuevo):
        return stock.id_producto == stockNuevo['id_producto'] and stock.lote == stockNuevo['lote']

    @classmethod
    def modificarStockExistente(cls,stockExistente,nuevoProducto):
        productoEnStock = cls.busquedaEnProducto(stockExistente.producto,nuevoProducto) 
        if(productoEnStock):
            print('hay coincidencia con espacio fisico y conteneredir')
            cls.modificarUnidades(productoEnStock[0],productoEnStock[0].unidad+nuevoProducto['unidad'])
        else:
            cls.crearProductoEnStock(stockExistente,nuevoProducto)
            print('no hubo coincidencia con esp fisico o cont me creo una nueva instancia de prod')
        return {'Status':'ok'},200 
  
    @classmethod
    def busquedaEnProducto(cls,productos,datos):
        return list(filter(lambda x: cls.criterioBusquedaProducto(x,datos) , productos))

    def criterioBusquedaProducto(producto,productoNuevo):
        return producto.id_espacioFisico == productoNuevo['id_espacioFisico'] and producto.codigoContenedor == productoNuevo['codigoContenedor']

    @classmethod
    def modificarUnidades(cls,producto,unidad):
        print('se encuentra stock con mismo lote y mismo id espacio fisico modif unidades')
        producto.unidad= unidad
    
    #deberia en service de producto en stock
    @classmethod
    def crearProductoEnStock(cls,stockExistente,datos):
        print(datos)
        stockExistente.producto.append(NuevoProductoEnStockSchema().load(datos))

    @classmethod
    def crearStock(cls,datos,grupoTrabajo):
        grupoTrabajo.stock.append(NuevoStockSchema().load(datos['stock']))
    
    def jsonMany(datos):
        return jsonify(StockSchema().dump(datos,many=True))
    def json(datos):
        return StockSchema().dump(datos)

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo):
        grupo = GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)
        if (grupo):
            return cls.jsonMany(grupo.stock)
        return  {'error':'Grupo de trabajo inexistente'},400

    #def busquedaPorId():
    @classmethod
    def borrarProductoEnStock(cls,datos):
        '''recibe un json con id grupo de trabajo, id de stock e id de producto en stock,
        si hay coincidencia lo borra'''

        



