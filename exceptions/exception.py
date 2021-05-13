

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

