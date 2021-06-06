from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.espacioFisicoService import EspacioFisicoService

from servicios.fuenteExperimentalService import FuenteExperimentalService

class EspacioFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().altaEspacioFisico(datos)
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(datos)
        return {'name': 'None'},400

class EspacioFisicoID(Resource):
    def get(self,id_espacioFisico):
        return EspacioFisicoService().obtenerEspacio(id_espacioFisico)

    def put(self,id_espacioFisico):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(id_espacioFisico)
        return {'name': 'None'},400
        
class CrearBlogEspacioFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(datos)
        return {'name': 'None'},400

class BorrarBlogEspacioFisico(Resource):
    def delete(self,id_espacioFisico,id_blog):
        datos = request.get_json()
        if(datos):
            return EspacioFisicoService().modificarEspacio(id_espacioFisico,id_blog)
        return {'name': 'None'},400

    @classmethod
    def nuevoBlogJaula(cls, datos):
            NuevoBlogJaulaSchema().load(datos)
            jaula = cls.find_by_id(datos['id_jaula'])
            blog = BlogService.nuevoBlog(datos['blogs'])
            jaula.blogs.append(blog)
            jaula.save()
            return {'Status':'Ok'}, 200
    @classmethod
    def borrarBlogJaula(cls,_id_jaula,_id_blog):
        if(Jaula.objects.filter(id_jaula = _id_jaula).first()):
            if (Jaula.objects.filter(id_jaula = _id_jaula, blogs__id_blog= _id_blog).first()):
                return Jaula.objects.filter(id_jaula = _id_jaula).first().modify(pull__blogs__id_blog =_id_blog)
            raise ErrorBlogInexistente(_id_blog)
        raise ErrorJaulaInexistente(_id_jaula)
