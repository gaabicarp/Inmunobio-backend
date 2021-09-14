from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request, jsonify
from servicios.jaulaService import JaulaService
from schemas.jaulaSchema import  JaulaSchema
from servicios.commonService import CommonService

class Jaula(Resource):

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.crearJaula(datos)
                return {"Status": "Jaula creada."}, 200
            except Exception as err:
                return {"Error": err.args}, 400
        return  {'Error':'Se deben enviar datos para la creación de la jaula.'},400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.actualizarJaula(datos)
                return {"status": "Jaula modificada"}, 200
            except Exception as err:
                return {"Error": err.args}, 400
        return  {'Error':'Se deben enviar datos para la modificion de la jaula.'},400

    def delete(self, id_jaula):
        if id_jaula:
            try:
                JaulaService.bajarJaula(id_jaula)
                return {"Status" : "Se dió de baja la jaula."}, 200
            except Exception as err:
                return {"Error": err.args}, 400
        return {'Error': 'Se debe indicar un id para la jaula.'}, 400

class JaulasSinProyecto(Resource):
    def get(self):
        return CommonService.jsonMany(JaulaService.jaulasSinAsignar(),JaulaSchema)

class JaulasDelProyecto(Resource):
    def get(self, idProyecto):
        if(idProyecto):
            return CommonService.jsonMany(JaulaService.jaulasDelProyecto(idProyecto),JaulaSchema)
        return {'Error':'Se deben enviar id de proyecto válido.'},400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.actualizarProyectoDeLaJaula(datos)
                return {"status" : "Se asignó la jaula al proyecto."}, 200
            except Exception as err:
                return {"Error": err.args}, 400
        return  {'Error':'Se deben enviar datos para la modificación de la jaula.'},400

class BlogJaula(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                JaulaService.nuevoBlogJaula(datos) 
                return {'Status':'Se creó el blog de jaula.'}, 200      
            except Exception as err:
                return {"Error": err.args}, 400
        return {"Error" : "Deben indicarse datos para el blog"}, 400

class ObtenerBlogsJaula(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return JaulaService.obtenerBlogsDeJaula(datos)       
            except Exception as err:
                return {"Error": err.args}, 400
        return {"Error" : "Deben indicarse datos para el blog"}, 400

class JaulasBlogs(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                return JaulaService.blogsDeTodasLasJaulas(datos)  
            except Exception as err:
                return {"Error": err.args}, 400
        return {"Error" : "Deben indicarse datos para el blog"}, 400

class Jaulas(Resource):
    def get(self):
        try:
            return jsonify(JaulaService.obtenerTodasLasJaulas())
        except Exception as err:
            return {"Error": err.args}, 400

class JaulaXId(Resource):
    def get(self, id_jaula):
        if id_jaula:
            try:
                #obtener nombre del proyecto y asignarlo en este momento, no guardarlo
                return  CommonService.json(JaulaService.obtenerJaula(id_jaula),JaulaSchema)
            except Exception as err:
                return {"Error": err.args}, 400
        return {"Error" : "Se debe indicar el id de una jaula."}, 400

class BorrarBlogJaula(Resource):
    def delete(self,id_jaula,id_blog):
        try:
            JaulaService.borrarBlogJaula(id_jaula,id_blog)      
            return {"Status" : "Se dio de baja el blog de jaula"}, 200
        except Exception as err:
            return {"Error": err.args}, 400
