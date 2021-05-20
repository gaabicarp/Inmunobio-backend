from marshmallow import ValidationError,EXCLUDE
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema,busquedaStocksSchema,ModificarProducto
from schemas.productosEnStockSchema import NuevoProductosEnStockSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.productoService import ProductoService
from exceptions.exception import ErrorGrupoInexistente,ErrorProductoInexistente,ErrorStockEspacioFisicoInexistente,ErrorProductoEnStockInexistente,ErrorStockInexistente
from servicios.commonService import CommonService
from servicios.productosEnStockService import ProductoEnStockService

#TO- DO : testear unidades por agrupacion , tomar la descripcion del ultimo que se envia si coincide con otros stocks activos
"""
{
    id_grupoDeTrabajo: int
    id_espacioFisico: int
    id_producto: int 
    producto = [
        {
            id_productos =  fields.Integer(dump_only=True)
            codigoContenedor = fields.Integer()
            detalleUbicacion = fields.String(default="")
            unidad =fields.Integer(default=0)
            lote = fields.String(default="")
            fechaVencimiento = fields.DateTime()
        }
    ]
}

"""
class StockService():
    @classmethod
    def nuevoStock(cls,datos):
        try:
            NuevoStockSchema().load(datos)
            cls.validarNuevoStock(datos)
            productoEnSistema = ProductoService.find_by_id(datos['id_producto']) 
            return cls.altaStock(datos,productoEnSistema)
        except ValidationError as err:
            return {'error': err.messages},400
            #ver como anidar estos dos errores 
        except ErrorGrupoInexistente as err:
            return {'error':err.message},400
        except ErrorProductoInexistente as err:
            return {'error':err.message},400

    @classmethod
    def validarNuevoStock(cls,datos):
        GrupoDeTrabajoService.find_by_id(datos['id_grupoDeTrabajo']) 
        #EspacioFisicoService.find_by_id...

    @classmethod
    def altaStock(cls,datos,productoEnSistema):
        try:
            stock = cls.busquedaProductoActivoEnStock(datos)
            cls.altaProductoEnStock(stock,datos,productoEnSistema)
        except ErrorProductoInexistente :
            cls.crearStock(datos,productoEnSistema)
        return {'Status':'ok'},200

    @classmethod
    def busquedaProductoActivoEnStock(cls,datos):
        resultado = cls.BusquedaEnStockAlta(datos['id_grupoDeTrabajo'],datos['id_espacioFisico'],datos['id_producto']).first()
        return resultado

    def BusquedaEnStockAlta(_id_grupoDeTrabajo,_id_espacioFisico,_id_producto):
        #ver como concatener el filtro de busquedanEn STock y agregarle id_producto 
        resultado =  Stock.objects.filter(id_producto=_id_producto,id_espacioFisico = _id_espacioFisico, id_grupoDeTrabajo =_id_grupoDeTrabajo)
        if(not resultado):
            raise ErrorProductoInexistente()
        return resultado

    def BusquedaEnStock(_id_grupoDeTrabajo,_id_espacioFisico):
        resultado =  Stock.objects.filter(id_espacioFisico = _id_espacioFisico, id_grupoDeTrabajo =_id_grupoDeTrabajo )
        if(not resultado):
            raise ErrorStockEspacioFisicoInexistente()
        return resultado

    def busquedaProductoEnStock(stock,productoNuevo):
        for producto in stock:
            if(ProductoEnStockService().compararProductos(producto,productoNuevo)):
                 return producto
        return None
    @classmethod
    def BusquedaEnStockPorId(cls,_id_productoEnStock):
        resultado =  Stock.objects.filter(id_productoEnStock =_id_productoEnStock)
        #resultado =  Stock.objects.filter(producto__id_productos = _id_productos, id_productoEnStock =_id_productoEnStock ).first()
        print(resultado)
        if(not resultado):
            raise ErrorStockInexistente()
        return resultado

    @classmethod
    def busquedaProductoEnStockPorID(cls,_id_productos,_id_productoEnStock):
        resultado = cls.BusquedaEnStockPorId(_id_productoEnStock).filter(producto__id_productos=_id_productos).first()
        print(resultado)
        if(not resultado):
            raise ErrorProductoEnStockInexistente()
        return resultado

    @classmethod
    def crearProducto(cls,datos, productoEnSistema):
        productoNuevo = NuevoProductosEnStockSchema().load(datos,unknown=EXCLUDE )
        cls.setearUnidadesDeAgrupacion(productoEnSistema,productoNuevo)
        return productoNuevo

    @classmethod
    def altaProductoEnStock(cls,stock,datos,productoEnSistema):
        productoNuevo = cls.crearProducto(datos['producto'][0],productoEnSistema)
        productoEnStock = cls.busquedaProductoEnStock(stock.producto,productoNuevo)
        if not productoEnStock:
            stock.producto.append(productoNuevo)
        else:
            cls.modificarUnidades(productoEnStock.unidad + productoNuevo.unidad,productoEnStock)
        stock.save()
        return {'Status':'ok'},200

    @classmethod
    def modificarUnidades(cls,unidad,producto):
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
        try:
            GrupoDeTrabajoService.find_by_id(id_grupoDeTrabajo) #valido q exista grupo
            #faltabuscar espaciofisico y si no encuentra lanza excep
            stock =  cls.BusquedaEnStock(id_grupoDeTrabajo,id_espacioFisico)
            return CommonService.jsonMany(stock,StockSchema)
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400
        except ErrorStockEspacioFisicoInexistente as err:
            return {'Error':err.message},400


    @classmethod
    def borrarProductoEnStock(cls,datos):
        '''recibe un json con id de stock e id de producto en stock,
        si hay coincidencia lo borra'''
        try:
            busquedaStocksSchema().load(datos)
            stock= cls.busquedaProductoEnStockPorID(datos['id_productos'],datos['id_productoEnStock'])
            stock.update(pull__producto__id_productos = datos['id_productos'])
            stock= cls.BusquedaEnStockPorId(datos['id_productoEnStock']).first() #aca tengo que consultar de nuevo
            #porque los cambios se guardan en la base y no en el stock objeto, ver como se puede mejorar
            if(not stock.producto): stock.delete()
            stock.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400 
        except (ErrorProductoEnStockInexistente,ErrorStockInexistente) as err:
            return {'Error':err.message},400  

    def obtenerProductosEspecificos(_id_productos,productos):
        for prod in productos:
            if prod.id_productos == _id_productos: return prod
        raise ErrorProductoInexistente()
        

    @classmethod    
    def modificarProductoEnStock(cls,datos):
        try:
            ModificarProducto().load(datos)
            stock= cls.busquedaProductoEnStockPorID(datos['id_productos'],datos['id_productoEnStock'])
            producto = cls.obtenerProductosEspecificos(datos['id_productos'],stock.producto)
            CommonService.updateAtributes(producto,datos['producto'],'id_productos')
            stock.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except (ErrorProductoInexistente,ErrorProductoEnStockInexistente) as err:
            return {'Error':err.message},400  
        

    #para testear
    def borrarTodo(_id_grupoDeTrabajo):
        Stock.objects.filter(id_grupoDeTrabajo = _id_grupoDeTrabajo).delete()
        return {'Status':'ok'},200


