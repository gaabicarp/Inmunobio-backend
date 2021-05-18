

class ErrorProductoInexistente(Exception):
    def __init__(self, message="Producto inexistente"):
        self.message = message
        super().__init__(self.message)


class ErrorDistribuidoraInexistente(Exception):
    def __init__(self, message="Distribuidora inexistente"):
        self.message = message
        super().__init__(self.message)


class ErrorGrupoInexistente(Exception):
    def __init__(self, message="Grupo de trabajo inexistente"):
        self.message = message
        super().__init__(self.message)


class ErrorStockEspacioFisicoInexistente(Exception):
    def __init__(self, message="No hay stock activo para este id de espacio fisico "):
        self.message = message
        super().__init__(self.message)

class ErrorProductoEnStockInexistente(Exception):
    def __init__(self, message="No hay productos asociados con esa id_productos/id_productosEnStock  "):
        self.message = message
        super().__init__(self.message)