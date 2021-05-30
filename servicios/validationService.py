from models.mongo.proyecto import Proyecto



class ValidacionesUsuario():
    @classmethod
    def desvincularDeProyectos(cls,id_usuario):
        proyectos = Proyecto.objects.update(pull__participantes=id_usuario)
