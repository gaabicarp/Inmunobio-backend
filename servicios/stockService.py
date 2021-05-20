from marshmallow import ValidationError,EXCLUDE
from models.mongo.stock import Stock
from schemas.stockSchema import StockSchema,NuevoStockSchema,busquedaStocksSchema
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

    def busquedaProductoEnStockPorID(_id_productos,_id_productoEnStock):
        resultado = StockService().BusquedaEnStockPorId(_id_productoEnStock).filter(producto__id_productos=_id_productos).first()
        print(resultado)
        if(not resultado):
            raise ErrorProductoEnStockInexistente()
        return resultado

      
    @classmethod
    def altaProductoEnStock(cls,stock,datos,productoEnSistema):
        productoNuevo = NuevoProductosEnStockSchema().load(datos['producto'][0],unknown=EXCLUDE )
        cls.setearUnidadesDeAgrupacion(productoEnSistema,productoNuevo)
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
        print(CommonService.json(nuevoStock,StockSchema))

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
            stock= cls.BusquedaEnStockPorId(datos['id_productoEnStock']).first()
            if(not stock.producto): stock.delete()
            stock.save()
            return {'Status':'ok'},200
        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorProductoInexistente as err:
            return {'Error':err.message},400  
        except (ErrorProductoEnStockInexistente,ErrorStockInexistente) as err:
            return {'Error':err.message},400  



    @classmethod    
    def modificarProductoEnStock(cls,datos):
        try:
            ModificarProducto().load(datos)
            grupo = cls.obtenerGrupo(datos)
            producto,stockDeProducto,stock= cls.obtenerProductosEspecificos(datos,grupo)
            CommonService.updateAtributes(producto,datos,'id_productos')
            grupo.save()

        except ValidationError as err:
            return {'error': err.messages},400
        except ErrorGrupoInexistente as err:
            return {'Error':err.message},400
        except ErrorStockEspacioFisicoInexistente as err:
            return {'Error':err.message},400  
        except ErrorProductoInexistente as err:
            return {'Error':err.message},400  

    def borrarTodo(_id_grupoDeTrabajo):
        Stock.objects.filter(id_grupoDeTrabajo = _id_grupoDeTrabajo).delete()
        return {'Status':'ok'},200


    """     @classmethod
    def obtenerProductosEspecificos(cls,datos):
        stock = cls.busquedaEnStock(grupo.stock,datos['id_espacioFisico'],cls.filtrarPorEspacioFisico)
        if(stock):
            stockDeProducto = cls.busquedaEnStock(stock.productos,datos['id_productoEnStock'],cls.filtrarPorIdProducto)
            if(stockDeProducto):
                producto = cls.busquedaEnStock(stockDeProducto.producto,datos['id_productos'],cls.filtrarPorIdProductos)
                if(producto):
                    return producto,stockDeProducto,stock
            raise ErrorProductoInexistente()
        raise ErrorStockEspacioFisicoInexistente() """

    """     @classmethod
    def BusquedaProductoEnStock(cls,datos):
        try:
            resultado = cls.BusquedaEnStock(datos['id_grupoDeTrabajo'],datos['id_espacioFisico'])
            return resultado.filter(id_producto = datos['id_producto']).first()
        except ErrorStockEspacioFisicoInexistente():
            return None
    """

    """     def crearProductos(nuevoProducto):
        nuevoProductos = NuevoProductosSchema().load(nuevoProducto,unknown=EXCLUDE )
        productoEnStock.producto.append(nuevoProductos)
    """
    """     @classmethod
    def stockSegunEspacioFisico(cls,_id_grupoDeTrabajo,_id_espacioFisico):
        grupo = GrupoDeTrabajo.objects.filter(id_grupoDeTrabajo=_id_grupoDeTrabajo,stock__id_espacioFisico= _id_espacioFisico).first()
        if (not grupo):
            raise ErrorStockEspacioFisicoInexistente()
        return cls.busquedaEnStock(grupo.stock,_id_espacioFisico,cls.filtrarPorEspacioFisico) """

    """     @classmethod
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
        
            
    """

