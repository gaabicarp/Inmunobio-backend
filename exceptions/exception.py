class Error(Exception):
    """Base class for other exceptions"""
    pass


class ErrorProductoInexistente(Exception):
    def __init__(self, message="Producto inexistente"):
        self.message = message
        super().__init__(self.message)


