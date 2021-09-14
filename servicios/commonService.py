from flask import jsonify
class CommonService():
    
    def updateAtributes(object,atribute,keyExclude = []):
        for key,value in atribute.items():
            if key not in keyExclude and hasattr(object, key) :
                setattr(object, key, value)
  
    def comparar(objeto,otroObjeto,atributos):
        for att in atributos:
            if (getattr(objeto,att) != getattr(otroObjeto,att)): return False
        return True

    def jsonMany(datos,schema):
        return jsonify(schema().dump(datos,many=True))
    
    def json(datos,schema):
        return schema().dump(datos)
    
    @classmethod
    def asignarNombreEspacioFisico(cls,objeto):
        from servicios.espacioFisicoService import EspacioFisicoService
        return cls.asignarNombreAObjeto(objeto,EspacioFisicoService.obtenerNombreEspacioFisico, objeto['id_espacioFisico'],'nombreEspFisico')

    @classmethod
    def asignarNombreProyecto(cls,objeto):
        from servicios.proyectoService import ProyectoService
        return cls.asignarNombreAObjeto(objeto,ProyectoService.obtenerNombreProyecto, objeto['id_proyecto'],'nombreProyecto')

    @classmethod
    def asignarNombreExperimento(cls,objeto):
        from servicios.experimentoService import ExperimentoService
        return cls.asignarNombreAObjeto(objeto,ExperimentoService.nombreExperimento, objeto['id_experimento'],'codigoExperimento')
   
    @classmethod
    def asignacionNombresDistribuidora(cls,objeto):
        from servicios.distribuidoraService import DistribuidoraService
        return cls.asignarNombreAObjeto(objeto,DistribuidoraService.obtenerNombreDistribuidora, objeto['id_distribuidora'],'nombreDistribuidora',)

    @classmethod
    def asignarNombreContenedor(cls,objeto):
        from servicios.contenedorService import ContenedorService
        return cls.asignarNombreAObjeto(objeto,ContenedorService.obtenerNombreContenedor, objeto['codigoContenedor'],'nombreContenedor',)

    @classmethod
    def asignarNombreContenedorAux(cls,objeto):
        from servicios.contenedorService import ContenedorService
        if objeto: cls.asignarNombreAObjeto(objeto,ContenedorService.obtenerNombreContenedor, objeto['id_contenedor'],'nombreContenedor',) 
        return objeto

    @classmethod
    def asignarNombreProducto(cls,objeto):
        from servicios.productoService import ProductoService
        return cls.asignarNombreAObjeto(objeto,ProductoService.obtenerNombreProducto, objeto['id_producto'],'nombre')
    
    @classmethod
    def asignarUsuario(cls,objeto):
        from servicios.usuarioService import UsuarioService
        objeto.id_usuario = UsuarioService.find_by_id_all(objeto.id_usuario)
        return objeto
        
    @classmethod
    def asignarNombreAObjeto(cls,objeto,functionGetNameOf, id,etiqueta):
        cls.asignaNombre(functionGetNameOf(id), etiqueta,objeto) if id else cls.asignaNombre(id, etiqueta,objeto)
        return objeto

    @classmethod
    def asignaNombre(cls,valor,clave,objeto):
        objeto[clave] = valor