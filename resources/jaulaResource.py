from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from exceptions.exception import ErrorJsonVacio
from servicios.jaulaService import JaulaService
from schemas.jaulaSchema import  JaulaSchema, NuevaJaulaSchema, ActualizarProyectoJaulaSchema, ActualizarJaulaSchema,NuevoBlogJaulaSchema
from marshmallow import ValidationError
from servicios.commonService import CommonService
from exceptions.exception import ErrorJaulaInexistente,ErrorBlogInexistente
from schemas.blogSchema import BlogSchema

class Jaula(Resource):

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.crearJaula(datos)
                return {"status": "Jaula creada."}, 200
            except ValidationError as err:
                return {'Error': err.messages},400
        return  {'Error':'Se deben enviar datos para la creación de la jaula.'},400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.actualizarProyectoDeLaJaula(datos)
                return {"status" : "Se asignó la jaula al proyecto"}, 200
            except ValidationError as err:
                return {"Error" : err.messages}, 400
        return  {'Error':'Se deben enviar datos para la modificación de la jaula.'},400

    def delete(self, id_jaula):
        if id_jaula:
            return JaulaService.bajarJaula(id_jaula)
        return {'Error': 'Se debe indicar un id para la jaula.'}, 400

class JaulasSinProyecto(Resource):

    def get(self):
        jaulas = JaulaService.jaulasSinAsignar()
        if jaulas:
            print(jaulas)
            return CommonService.jsonMany(jaulas,JaulaSchema)
        else:
            return {"Status" : "No hay jaulas disponibles."}, 200

class JaulasDelProyecto(Resource):

    def get(self, idProyecto):
        jaulas = JaulaService.jaulasDelProyecto(idProyecto)
        if jaulas:
            return jaulas, 200
        else:
            return {"Status" : "No hay jaulas asignadas a ese proyecto."}, 200

class BlogJaula(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return JaulaService.nuevoBlogJaula(datos)       
            except ValidationError as err:
                return {"Error" : err.messages}, 400
            except ErrorJaulaInexistente as err:
                return {'Error':err.message},400 
        return {"Status" : "Deben indicarse datos para el blog"}, 400

class ObtenerBlogsJaula(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                blogs = JaulaService.obtenerBlogs(datos)       
                return CommonService.jsonMany(blogs,BlogSchema)
            except ValidationError as err:
                return {"Error" : err.messages}, 400
            except ErrorJaulaInexistente as err:
                return {'Error':err.message},400 
        return {"Status" : "Deben indicarse datos para el blog"}, 400

class BorrarBlogJaula(Resource):
    def delete(self,id_jaula,id_blog):
        try:
            JaulaService.borrarBlogJaula(id_jaula,id_blog)      
            return {"Status" : "Ok"}, 200
        except ErrorJaulaInexistente as err:
            return {'Error':err.message},400 
        except (ErrorBlogInexistente,ErrorJaulaInexistente) as err:
            return {'Error':err.message},400

class Jaulas(Resource):
    def get(self):
        try:
            return  CommonService.jsonMany(JaulaService.obtenerJaulas() ,JaulaSchema)
        except ErrorJaulaInexistente as err:
            return {'Error':err.message},400 
        except (ErrorBlogInexistente,ErrorJaulaInexistente) as err:
            return {'Error':err.message},400

class JaulaXId(Resource):
    def get(self, id_jaula):
        if id_jaula:
            try:
                return  CommonService.json(JaulaService.find_by_id(id_jaula),JaulaSchema)
            except ErrorJaulaInexistente as err:    
                return {'Error':err.message},400 
        return {"Error" : "Se debe indicar el id de una jaula."}, 400