from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request, jsonify

from marshmallow import ValidationError
from exceptions.exception import ErrorProyectoInexistente,ErrorJaulaBaja,ErrorEspacioDeproyecto
from servicios.jaulaService import JaulaService
from schemas.jaulaSchema import  JaulaSchema
from marshmallow import ValidationError
from servicios.commonService import CommonService
from exceptions.exception import ErrorJaulaInexistente,ErrorBlogInexistente,ErrorFechasInvalidas
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
                JaulaService.actualizarJaula(datos)
                return {"status": "Jaula modificada"}, 200
            except ValidationError as err:
                return {'Error': err.messages},400
            except ErrorJaulaInexistente as err:
                return {'Error':err.message},400 
        return  {'Error':'Se deben enviar datos para la modificion de la jaula.'},400

    def delete(self, id_jaula):
        if id_jaula:
            try:
                JaulaService.bajarJaula(id_jaula)
                return {"Status" : "Ok"}, 200
            except (ErrorJaulaBaja,ErrorJaulaInexistente) as err:
                return {'Error':err.message},400 
        return {'Error': 'Se debe indicar un id para la jaula.'}, 400

class JaulasSinProyecto(Resource):
    def get(self):
        jaulas = JaulaService.jaulasSinAsignar()
        return CommonService.jsonMany(jaulas,JaulaSchema)

class JaulasDelProyecto(Resource):
    def get(self, idProyecto):
        jaulas = JaulaService.jaulasDelProyecto(idProyecto)
        print(jaulas)
        return CommonService.jsonMany(jaulas,JaulaSchema)

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.actualizarProyectoDeLaJaula(datos)
                return {"status" : "Se asignó la jaula al proyecto"}, 200
            except ValidationError as err:
                return {"Error" : err.messages}, 400
            except ErrorProyectoInexistente as err:
                return {'Error':err.message},400 
        return  {'Error':'Se deben enviar datos para la modificación de la jaula.'},400

class BlogJaula(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.nuevoBlogJaula(datos) 
                return {'Status':'Ok'}, 200      
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

class JaulasBlogs(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return JaulaService.obtenerTodosLosBlogs(datos)  
            except (ErrorFechasInvalidas,ErrorProyectoInexistente) as err:
                return {'Error':err.message},400 
        return {"Status" : "Deben indicarse datos para el blog"}, 400

class BorrarBlogJaula(Resource):
    def delete(self,id_jaula,id_blog):
        try:
            JaulaService.borrarBlogJaula(id_jaula,id_blog)      
            return {"Status" : "Ok"}, 200
        except (ErrorBlogInexistente,ErrorJaulaInexistente) as err:
            return {'Error':err.message},400

class Jaulas(Resource):
    def get(self):
        try:
            return jsonify(JaulaService.obtenerJaulas())
        except (ErrorJaulaInexistente,ErrorProyectoInexistente,ErrorEspacioDeproyecto) as err:
            return {'Error':err.message},400

class JaulaXId(Resource):
    def get(self, id_jaula):
        if id_jaula:
            try:
                #obtener nombre del proyecto y asignarlo en este momento, no guardarlo
                jaula = JaulaService.obtenerJaula(id_jaula)
                return  CommonService.json(jaula,JaulaSchema)
            except (ErrorJaulaInexistente,ErrorProyectoInexistente) as err:    
                return {'Error':err.message},400 
        return {"Error" : "Se debe indicar el id de una jaula."}, 400