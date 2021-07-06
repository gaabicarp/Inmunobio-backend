

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

class ErrorEspacioFisicoInexistente(Exception):
    def __init__(self,id, message="No existe espacio fisico con id "):
        self.message = message + str(id)
        super().__init__(self.message)


class ErrorUnidadStock(Exception):
    def __init__(self, message="Las unidades de Stock deben ser numeros enteros positivos "):
        self.message = message
        super().__init__(self.message)

class ErrorPermisoInexistente(Exception):
    def __init__(self,id_permiso, message="No hay permisos asociados con id "):
        self.message = message + str(id_permiso)
        super().__init__(self.message)

class ErrorUsuarioInexistente(Exception):
    def __init__(self,id_usuario, message="No hay usuario asociados con id "):
        self.message = message + str(id_usuario)
        super().__init__(self.message)

class ErrorGrupoDeTrabajoGeneral(Exception):
    def __init__(self, message="El grupo es general y no puede darse de baja."):
        self.message = message 
        super().__init__(self.message)


class ErrorJsonVacio(Exception):
    def __init__(self, message="Error en el envio de datos"):
        self.message = message 
        super().__init__(self.message)

class ErrorJaulaInexistente(Exception):
    def __init__(self,id_jaula, message="No se encontró ninguna jaula con el id: "):
        self.message = message + str(id_jaula)
        super().__init__(self.message)    

class ErrorBlogInexistente(Exception):
    def __init__(self,id_blog, message="No se encontró ninguna blog con el id: "):
        self.message = message + str(id_blog)
        super().__init__(self.message)    


class ErrorHerramientaInexistente(Exception):
    def __init__(self,id_herr, message="No se encontró ninguna herramienta con el id: "):
        self.message = message + str(id_herr)
        super().__init__(self.message)    

class ErrorProyectoInexistente(Exception):
    def __init__(self,id_herr, message="No se encontró ningun proyecto con el id: "):
        self.message = message + str(id_herr)
        super().__init__(self.message)    
class ErrorFechasInvalidas(Exception):
    def __init__(self, message="La fecha-desde debe ser inferior a la fecha-hasta "):
        self.message = message 
        super().__init__(self.message)    

class ErrorJaulaBaja(Exception):
    def __init__(self, message="La jaula debe estar vacía para poder darla de baja "):
        self.message = message 
        super().__init__(self.message)    

class ErrorJaulaDeProyecto(Exception):
    def __init__(self,id_proyecto,id_jaula):
        self.message = "La jaula "  + str(id_jaula)+" no se encuentra asignada al proyecto con id " + str(id_proyecto)
        super().__init__(self.message)   

class ErrorExpDeProyecto(Exception):
    def __init__(self,id_proyecto,id_experimento):
        self.message = "El experimento "  + str(id_experimento)+" no se encuentra asignada al proyecto con id " + str(id_proyecto)
        super().__init__(self.message)    

class ErrorExperimentoInexistente(Exception):
    def __init__(self,id_experimento):
        self.message = "No existe experimento asociado con id  "  + str(id_experimento)
        super().__init__(self.message)    
class ErrorContenedorInexistente(Exception):
    def __init__(self,id_contenedor):
        self.message = "No existe contenedor asociado con id "  + str(id_contenedor)
        super().__init__(self.message)    

class ErrorEspacioDeproyecto(Exception):
    def __init__(self,id_espFisico,id_proyecto):
        self.message = "El espacio fisico con id."  + str(id_espFisico) + " asociado al proyecto id."+str(id_proyecto)+" ya no se encuentra disponible"
        super().__init__(self.message)  

class ErrorNombreInvalido(Exception):
    def __init__(self):
        self.message = ""
        super().__init__(self.message)      
       
        