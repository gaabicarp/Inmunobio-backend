#from dateutil import parser
#import datetime
from marshmallow import ValidationError,EXCLUDE
from flask import jsonify
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema
from schemas.productosSchema import NuevoProductosSchema
from schemas.productoEnStockSchema import NuevoProductoEnStockSchema
from schemas.grupoTrabajoSchema import GrupoDeTrabajoSchema, NuevoStockGrupoSchema,busquedaStocksSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.productoService import ProductoService
from exceptions.exception import ErrorGrupoInexistente,ErrorProductoInexistente
from models.mongo.grupoDeTrabajo import GrupoDeTrabajo
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
        print(datos)
        nuevoProductoEnStock=NuevoProductoEnStockSchema().load(datos,unknown=EXCLUDE)
        stockExistente.productos.append(nuevoProductoEnStock)


    def crearProductos(productoEnStock,nuevoProducto):
        nuevoProductos = NuevoProductosSchema().load(nuevoProducto,unknown=EXCLUDE )
        productoEnStock.producto.append(nuevoProductos)

    def jsonMany(datos):
        return jsonify(StockSchema().dump(datos,many=True))

    def json(datos):
        return StockSchema().dump(datos)

    @classmethod
    def obtenerProductos(cls,id_grupoDeTrabajo,id_espacioFisico):
        try:
            #faltabusca espaciofisico y si no encuentra lanza excep
            grupo =  cls.stockSegunEspacioFisico(id_grupoDeTrabajo,id_espacioFisico)
            return cls.jsonMany(grupo)
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400

    def stockSegunEspacioFisico(_id_grupoDeTrabajo,_id_espacioFisico):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=_id_grupoDeTrabajo).fields(stock = {'$elemMatch': {'id_espacioFisico': _id_espacioFisico}})
        print(grupo)
        return grupo
        #Sku.objects(variants__match={ "name": "xxx", "value": "xxx" })


    @classmethod
    def obtenerStocks(cls,_id_grupoDeTrabajo):     
        return cls.jsonMany(GrupoDeTrabajoService.find_by_id(_id_grupoDeTrabajo).stock)


    #def busquedaPorId():
    @classmethod
    def borrarProductoEnStock(cls,datos):
        '''recibe un json con id grupo de trabajo, id de stock e id de producto en stock,
        si hay coincidencia lo borra'''
        grupo = GrupoDeTrabajoService.find_by_id(1)
        grupo.stock = []
        grupo.save()


        



