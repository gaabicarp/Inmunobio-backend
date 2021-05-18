from marshmallow import ValidationError,EXCLUDE
from schemas.stockSchema import StockSchema,NuevoStockSchema
from schemas.productosEnStockSchema import NuevoProductosEnStockSchema
from servicios.grupoDeTrabajoService import GrupoDeTrabajoService
from servicios.productoService import ProductoService
from exceptions.exception import ErrorGrupoInexistente,ErrorProductoInexistente,ErrorStockEspacioFisicoInexistente
from models.mongo.grupoDeTrabajo import GrupoDeTrabajo
from servicios.commonService import CommonService


class ProductoEnStockService():
    
   
    def compararProductos(cls,objeto,otro):
        return CommonService.comparar(objeto,otro,['lote','codigoContenedor','fechaVencimiento'])
      