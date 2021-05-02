from dateutil import parser
import datetime
from marshmallow import Schema, ValidationError
from flask import jsonify, request
from models.mongo.productosStock import Stock,NuevoStockSchema,StockSchema
from models.mongo.grupoDeTrabajo import NuevoStockGrupoSchema,GrupoDeTrabajoIDSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService

class StockService:
    @classmethod
    def altaStock(cls,datos):
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
            grupoTrabajo.stock.append(cls.crearStock(datos))
            grupoTrabajo.save()
        return {'Status':'ok'},200 
  
    @classmethod
    def busquedaEnStock(cls,stocks,datos):
        '''Recibe lista con stocks y stock a dar de alta, devuelva un stock que coincida con los datos
        del stock a dar de alta,o null si no encuentra'''
        for 

    @classmethod
    def aumentarUnidades(cls,stock):
        pass

    @classmethod
    def crearStock(cls,datos):
        datos.pop('id_grupoDeTrabajo')
        print(datos)
        return NuevoStockSchema().load(datos['stock'])





