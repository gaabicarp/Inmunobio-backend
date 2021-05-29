

class ErrorProductoInexistente(Exception):
    def __init__(self,id, message="No hay productos relacionados con id_producto "):
        self.message = message + str(id)
        super().__init__(self.message)

class ErrorProductoEnStockInexistente(Exception):
    def __init__(self,id, message="No hay productos activos con id_productos "):
        self.message = message + str(id)
        super().__init__(self.message)

class ErrorStockVacio(Exception):
    def __init__(self, message= "Deben indicarse unidades positivas y mayores a cero"):
        self.message = message 
        super().__init__(self.message)

class ErrorStockInexistente(Exception):
    def __init__(self, message="Stock con id_productos inexistente"):
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


class ErrorUnidadStock(Exception):
    def __init__(self, message="Las unidades de Stock deben ser numeros enteros positivos "):
        self.message = message
        super().__init__(self.message)

class ErrorPermisoInexistente(Exception):
    def __init__(self,id_permiso, message="No hay permisos asociados con id "):
        self.message = message + str(id_permiso)
        super().__init__(self.message)

class ErrorPermisosInexistentes(Exception):
    def __init__(self, message="No hay permisos activos"):
        self.message = message 
        super().__init__(self.message)

class ErrorUsuarioInexistente(Exception):
    def __init__(self,id_usuario, message="No hay usuario asociados con id "):
        self.message = message + str(id_usuario)
        super().__init__(self.message)

class ErrorUsuariosInexistentes(Exception):
    def __init__(self,id_usuario, message="No hay usuario habilitados "):
        self.message = message + str(id_usuario)
        super().__init__(self.message)

class ErrorGrupoDeTrabajoGeneral(Exception):
    def __init__(self, message="El grupo es general y no puede darse de baja."):
        self.message = message 
        super().__init__(self.message)