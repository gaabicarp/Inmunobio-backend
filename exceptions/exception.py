
""" class ErrorProductoInexistente(Exception):
    def __init__(self,id):
        self.message = f"No hay productos relacionados con id_producto: {id}" 
        super().__init__(self.message) """

""" class ErrorProductoEnStockInexistente(Exception):
    def __init__(self,id=0):
        self.message = f"No hay productos activos con id_productos {id}"
        super().__init__(self.message)

class ErrorStockInexistente(Exception):
    def __init__(self,id):
        self.message = f"No existe stock asociado con id_productoEnStock {id}" 
        super().__init__(self.message)

class ErrorDistribuidoraInexistente(Exception):
    def __init__(self):
        self.message = "Distribuidora inexistente"
        super().__init__(self.message)

class ErrorGrupoInexistente(Exception):
    def __init__(self):
        self.message = "Grupo de trabajo inexistente"
        super().__init__(self.message) 

class ErrorEspacioFisicoInexistente(Exception):
    def __init__(self,id):
        self.message = f"No existe espacio fisico con id {id}" 
        super().__init__(self.message)

class ErrorPermisoInexistente(Exception):
    def __init__(self,id_permiso):
        self.message = f"No hay permisos asociados con id {id_permiso}" 
        super().__init__(self.message)


class ErrorBlogInexistente(Exception):
    def __init__(self,id_blog):
        self.message = f"No se encontró ningun blog con el id: {id_blog}"
        super().__init__(self.message)    

class ErrorHerramientaInexistente(Exception):
    def __init__(self,id_herr):
        self.message = f"No se encontró ninguna herramienta con el id: {id_herr}"
        super().__init__(self.message)    

class ErrorProyectoInexistente(Exception):
    def __init__(self,id_herr):
        self.message = f"No se encontró ningun proyecto con el id: {id_herr}"
        super().__init__(self.message)    

class ErrorFechasInvalidas(Exception):
    def __init__(self):
        self.message = "La fecha-desde debe ser inferior a la fecha-hasta " 
        super().__init__(self.message)    

class ErrorJaulaBaja(Exception):
    def __init__(self):
        self.message = "La jaula debe estar vacía para poder darla de baja " 
        super().__init__(self.message)    

class ErrorJaulaDeProyecto(Exception):
    def __init__(self,id_proyecto,id_jaula):
        self.message = f"La jaula {id_jaula} no se encuentra asignada al proyecto con id {id_proyecto}"
        super().__init__(self.message)   

class ErrorExpDeProyecto(Exception):
    def __init__(self,id_proyecto,id_experimento):
        self.message = f"El experimento {id_experimento} no se encuentra asignado al proyecto con id {id_proyecto}"
        super().__init__(self.message)    

class ErrorExperimentoInexistente(Exception):
    def __init__(self,id_experimento):
        self.message = f"No existe experimento asociado con id {id_experimento}"
        super().__init__(self.message)    
class ErrorContenedorInexistente(Exception):
    def __init__(self,id_contenedor):
        self.message = f"No existe contenedor asociado con id {id_contenedor}"
        super().__init__(self.message)    

class ErrorEspacioDeproyecto(Exception):
    def __init__(self,id_espFisico,id_proyecto):
        self.message = f"El espacio fisico con id.{id_espFisico} asociado al proyecto id.{id_proyecto} ya no se encuentra disponible"
        super().__init__(self.message)  
"""