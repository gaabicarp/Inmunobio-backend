from servicios.commonService import CommonService


class ProductoEnStockService():
    def compararProductos(cls,objeto,otro):
        return CommonService.comparar(objeto,otro,['lote','codigoContenedor','fechaVencimiento'])



       