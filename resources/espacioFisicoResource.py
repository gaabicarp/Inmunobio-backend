from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.espacioFisicoService import EspacioFisicoService
from exceptions.exception import ErrorEspacioFisicoInexistente,ErrorBlogInexistente,ErrorFechasInvalidas
from servicios.commonService import CommonService
from schemas.espacioFisicoSchema import EspacioFisicoSchema,NuevoBlogEspacioFisicoSchema
from schemas.blogSchema import BlogSchema
from marshmallow import ValidationError

class EspacioFisico(Resource):

    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                EspacioFisicoService().altaEspacioFisico(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                    return {'error': err.messages},400 
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if(datos): 
            try:           
                EspacioFisicoService().modificarEspacio(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400 
            except ErrorEspacioFisicoInexistente as err:
                return {'error':err.message},400
        return {'name': 'None'},400


class EspacioFisicoID(Resource):
    def get(self,id_espacioFisico):
        if id_espacioFisico:
            try:
                espacio = EspacioFisicoService().find_by_id(id_espacioFisico)
                return CommonService.json(espacio,EspacioFisicoSchema)
            except ValidationError as err:
                return {'error': err.messages},400 
            except ErrorEspacioFisicoInexistente as err:
                return {'error':err.message},400
        return {'name': 'None'},400


    def delete(self,id_espacioFisico):
        if(id_espacioFisico):
            try:
                EspacioFisicoService().borrarEspacio(id_espacioFisico)
                return {'Status':'ok'},200
            except ErrorEspacioFisicoInexistente as err:
                return {'error':err.message},400
        return {'Error': 'Parametros requeridos'},400

class CrearBlogEspacioFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                EspacioFisicoService().crearBlogEspacioFisico(datos)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},400 
            except ErrorEspacioFisicoInexistente as err:
                return {'error':err.message},400
        return {'Error': 'Error al decodificar json'},400

class BorrarBlogEspacioFisico(Resource):
    def delete(self,id_espacioFisico,id_blog):
        if id_espacioFisico and id_blog:
            try:
                EspacioFisicoService().BorrarBlogEspacioFisico(id_espacioFisico,id_blog)
                return {'Status':'ok'},200
            except (ErrorEspacioFisicoInexistente,ErrorBlogInexistente) as err:
                return {'error':err.message},400
        return {'Error': 'Parametros requeridos'},400

class ObtenerBlogsEspFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                blogs = EspacioFisicoService().obtenerBlogs(datos)
                return CommonService.jsonMany(blogs,BlogSchema)
            except (ErrorEspacioFisicoInexistente,ErrorFechasInvalidas) as err:
                return {'error':err.message},400
            except ValidationError as err:
                return {'error': err.messages},400            
        return {'Error': 'Parametros requeridos'},400
        
class EspaciosFisicos(Resource):
    def get(self): 
        return CommonService.jsonMany(EspacioFisicoService().obtenerEspacios(),EspacioFisicoSchema)




