from flask import jsonify
from exceptions.exception import ErrorNombreInvalido
class CommonService():
    
    def updateAtributes(object,atribute,keyExclude = ""):
        for key,value in atribute.items():
            if keyExclude != key and hasattr(object, key) :
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
    def asignacionNombresDistribuidora(cls,objeto):
        from servicios.distribuidoraService import DistribuidoraService
        return cls.asignarNombreAObjeto(objeto,DistribuidoraService.obtenerNombreDistribuidora, objeto['id_distribuidora'],'nombreDistribuidora',)

    @classmethod
    def asignarNombreContenedor(cls,objeto):
        from servicios.contenedorService import ContenedorService
        return cls.asignarNombreAObjeto(objeto,ContenedorService.obtenerNombreContenedor, objeto['codigoContenedor'],'nombreContenedor',)
        
    @classmethod
    def asignarNombreProducto(cls,objeto):
        from servicios.productoService import ProductoService
        return cls.asignarNombreAObjeto(objeto,ProductoService.obtenerNombreProducto, objeto['id_producto'],'nombre')

    @classmethod
    def asignarNombreAObjeto(cls,objeto,functionGetNameOf, id,etiqueta):
        try:
            cls.validarId(id)
            cls.asignaNombre(functionGetNameOf(id), etiqueta,objeto)
        except ErrorNombreInvalido as err:
            cls.asignaNombre(id, etiqueta,objeto)
        finally: return objeto

    @classmethod
    def validarId(cls,id):
        if not id : raise ErrorNombreInvalido

    @classmethod
    def asignaNombre(cls,valor,clave,objeto):
        objeto[clave] = valor