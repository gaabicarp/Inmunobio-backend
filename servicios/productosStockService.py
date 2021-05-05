#from dateutil import parser
#import datetime
from marshmallow import Schema, ValidationError
from flask import jsonify, request
from models.mongo.productosStock import ProductosStock,ProductosStockSchema,NuevoProductosStockSchema
from models.mongo.grupoDeTrabajo import NuevoStockGrupoSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService

class StockService:
    @classmethod
    def altaProductoEnStock(cls,datos):
        try:
            NuevoStockGrupoSchema().load(datos)
            grupoBuscado = GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo'])     
            if(grupoBuscado):
                return cls.modificarStock(grupoBuscado,datos)
            return  {'error':'Grupo de trabajo inexistente'},404
        except ValidationError as err:
            return {'error': err.messages},404


    @classmethod
    def modificarStock(cls,grupoTrabajo,datos):
        stockAgrupable = cls.busquedaEnStock(grupoTrabajo.stock,datos)
        if(stockAgrupable):
            #aumento stock
            print('aumentostocl')
            cls.aumentarUnidades(stockAgrupable)
        else:
            print('creo el stock y lo agrego al grupo')
            nuevoProductoStock = cls.crearProductoEnStock(datos))
            
            grupoTrabajo.save()
        return {'Status':'ok'},200 
  
    @classmethod
    def busquedaEnStock(cls,productos,datos):
        '''Recibe lista con stocks y stock a dar de alta, devuelva un stock que coincida con id_producto
        a dar de alta,o [] si no encuentra'''
        return filter(lambda x: x.id_producto == datos['id_producto'], productos)
    @classmethod
    def aumentarUnidades(cls,stock):
        pass

    @classmethod
    def crearProductoEnStock(cls,datos):
        print(datos)
        return NuevoProductosStockSchema().load(datos,unknown=EXCLUDE)





