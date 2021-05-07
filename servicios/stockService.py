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
        stockProducto = cls.busquedaEnStock(grupoTrabajo.stock,datos['stock'])
        if(stockProducto):
            #aumento stock
            print('aumentosto unidades')
            cls.aumentarUnidades(stockProducto,datos['stock'])
        else:
           cls.crearStock(datos,grupoTrabajo)
           
        return {'Status':'ok'},200 
  
    @classmethod
    def busquedaEnStock(cls,stocks,datos):
        '''Recibe lista con stocks y stock a dar de alta, devuelve un stock que coincida con id_producto
        a dar de alta,o [] si no encuentra'''
        return list(filter(lambda x: cls.criterioBusqueda(x,datos), stocks))
    

    def criterioBusqueda(stock,stockNuevo):
        return stock.id_producto == stockNuevo['id_producto'] and stock.lote == stockNuevo['lote']

    @classmethod
    def busquedaEnProducto(cls,productos,datos):
        return list(filter(lambda x: x.id_espacioFisico == datos['id_espacioFisico'], productos))

    @classmethod
    def aumentarUnidades(cls,producto,datos):
        if(cls.busquedaEnProducto(producto,datos['producto'][0]) ):
            print('se encuentra stock con mismo lote y mismo id espacio fisico aumento unidades')
        

    @classmethod
    def crearStock(cls,datos,grupoTrabajo):
        grupoTrabajo.stock.append(NuevoStockSchema().load(datos['stock']))
        grupoTrabajo.save()
    
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






