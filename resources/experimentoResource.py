from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from exceptions.exception import ErrorExperimentoInexistente,ErrorFechasInvalidas
from servicios.experimentoService import ExperimentoService
from servicios.commonService import CommonService
from schemas.experimentoSchema import NuevoBlogExpSchema, ExperimentoSchema, ModificarExperimentoSchema, AltaExperimentoSchema, CerrarExperimentoSchema, AgregarMuestrasAlExperimentoSchema
from schemas.blogSchema import BlogSchema
class Experimentos(Resource):

    #@jwt_required()
    def get(self, idProyecto):
        if idProyecto:
            experimentos = ExperimentoService().find_all_by_idProyecto(idProyecto)
            return experimentos, 200
        return {"Error" : "Se debe indicar un id del proyecto válido."}, 400

class ExperimentoResource(Resource):
    #@jwt_required()
    def get(self, idExperimiento):
        if idExperimiento:
            try:
                experimento = ExperimentoService().find_by_id(idExperimiento)
                return CommonService.json(experimento,ExperimentoSchema),200
            except ErrorExperimentoInexistente as err:
                return {'error': err.message}, 400
            except ValidationError as err:
                return {'error': err.messages}, 400
        return {"Error" : "Se debe indicar un id de experimento válido."}, 400

    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.nuevoExperimento(datos)
                return {"Status":"ok"}, 201
            except ValidationError as err:
                return {'error': err.messages},400
        return {"Error" : "Se deben enviar datos para la creación del experimento."}, 400

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.modificarExperimento(datos)
                return {"Status":"ok"}, 201
            except ValidationError as err:
                return {'Error': err.messages},400
        return {"Error" : "Se deben enviar datos para la actualización del experimento."}, 400

class CerrarExperimento(Resource):

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.cerrarExperimento(datos)
                return {"Status" : "ok"}
            except ValidationError as err:
                return {'Error': err.messages},400
        return {"Error" : "Se deben enviar datos para poder cerrar el experimento."}, 400

class ExperimentoMuestra(Resource):

    #@jwt_required()
    def put(self, datos):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.agregarMuestrasExternasAlExperimento(datos)
                return {"Status" : "Ok"}, 200
            except ValidationError as err:
                return {"Error" : err.messages}, 400
            except Exception as err:
                return {"Error" : str(err)}, 400
        return {"Error" : "Se deben enviar datos para poder agregar muestras."}, 400

class BlogExperimento(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.nuevoBlogExperimento(datos) 
                return {'Status':'Ok'}, 200      
            except ValidationError as err:
                return {"Error" : err.messages}, 400
            except ErrorExperimentoInexistente as err:
                return {'Error':err.message},400 
        return {"Status" : "Deben indicarse datos para el blog"}, 400

class ObtenerBlogsExp(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                blogs = ExperimentoService.obtenerBlogs(datos)
                return CommonService.jsonMany(blogs,BlogSchema)
            except (ErrorExperimentoInexistente,ErrorFechasInvalidas) as err:
                return {'error':err.message},400
            except ValidationError as err:
                return {'error': err.messages},400            
        return {'Error': 'Parametros requeridos'},400