#from dateutil import parser
#import datetime
from marshmallow import ValidationError,EXCLUDE
from flask import jsonify, request
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema
from schemas.grupoTrabajoSchema import NuevoStockGrupoSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService

class StockService():
    @classmethod
    def altaStock(cls,datos):
        try:
            NuevoStockGrupoSchema().load(datos)
            if(cls.validarNuevoStock(datos)):
                return cls.modificarStock(cls.obtenerGrupo(datos), datos)
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
    def modificarStock(cls,grupoTrabajo,datos):
        stockProducto = cls.busquedaEnStock(grupoTrabajo.stock,datos)
        print('imprimo stock del grupo')
        print(grupoTrabajo.stock)
        if(stockProducto):
            #aumento stock
            print('aumentosto unidades')
            cls.aumentarUnidades(stockProducto)
        else:
            print('creo el stock y lo agrego al grupo')
            nuevoStock = cls.crearStock(datos)
            print('PRINT NUEVO STOCK')
            print(nuevoStock)
            grupoTrabajo.stock.append(nuevoStock)
            grupoTrabajo.save()
        return {'Status':'ok'},200 
  
    @classmethod
    def busquedaEnStock(cls,productos,datos):
        '''Recibe lista con stocks y stock a dar de alta, devuelve un stock que coincida con id_producto
        a dar de alta,o [] si no encuentra'''
        print(list(filter(lambda x: x.id_producto == datos['id_producto'], productos)))
        return list(filter(lambda x: x.id_producto == datos['id_producto'], productos))

    @classmethod
    def aumentarUnidades(cls,stock):
        pass

    @classmethod
    def crearStock(cls,datos):
        print(datos)
        return NuevoStockSchema().load(datos['stock'])
    
    def jsonMany(datos):
        return jsonify(StockSchema().dump(datos,many=True))

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo):
        grupo = GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo)
        if (grupo):
            return cls.jsonMany(grupo.stock)
        return  {'error':'Grupo de trabajo inexistente'},400






