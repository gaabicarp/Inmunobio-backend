from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.experimentoService import ExperimentoService
from servicios.commonService import CommonService
from schemas.experimentoSchema import  ExperimentoSchema

class Experimentos(Resource):

    #@jwt_required()
    def get(self, idProyecto):
        if idProyecto:
            return ExperimentoService().find_all_by_idProyecto(idProyecto), 200
        return {"Error" : "Se debe indicar un id del proyecto válido."}, 400

class ExperimentoResource(Resource):
    def get(self, idExperimiento):
        if idExperimiento:
            try:
                return ExperimentoService().experimentoPorId(idExperimiento)
            except Exception as err:
                return {'Error': err.args}, 400
        return {"Error" : "Se debe indicar un id de experimento válido."}, 400

    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.nuevoExperimento(datos)
                return {"Status":"Se creó el experimento."}, 201
            except Exception as err:
                return {'Error': err.args}, 400
        return {"Error" : "Se deben enviar datos para la creación del experimento."}, 400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.modificarExperimento(datos)
                return {"Status":"Se modificó el experimento."}, 201
            except Exception as err:
                return {'error': err.args}, 400
        return {"Error" : "Se deben enviar datos para la actualización del experimento."}, 400

class CerrarExperimento(Resource):

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.cerrarExperimento(datos)
                return {"Status" : "Se cerró el experimento."}
            except Exception as err:
                return {'Error': err.args}, 400
        return {"Error" : "Se deben enviar datos para poder cerrar el experimento."}, 400

class ExperimentoMuestra(Resource):

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.agregarMuestrasExternasAlExperimento(datos)
                return {"Status" : "Se agregaron las muestras al experimento."}, 200
            except Exception as err:
                return {'Error': err.args}, 400
        return {"Error" : "Se deben enviar datos para poder agregar muestras."}, 400

    def delete(self, idExperimento, idMuestra):
        if idExperimento and idMuestra:
            try:
                ExperimentoService.removerMuestraDeExperimento(idExperimento, idMuestra)
                return {'Status':'Se removieron las muestras del experimento'}, 200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Se debe enviar el id del experimento y el id de la muestra.'}, 400
        
class BlogExperimento(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ExperimentoService.nuevoBlogExperimento(datos) 
                return {'Status':'SE creó el blog de experimento.'}, 200      
            except Exception as err:
                return {"Error" : err.args}, 400
        return {"Status" : "Deben indicarse datos para la creación del blog"}, 400

class ObtenerBlogsExp(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                return ExperimentoService.obtenerBlogsEXperimentoPorID(datos)
            except Exception as err:
                return {'Error' : err.args}, 400          
        return {'Error': 'Parametros id de experimento,fecha-desde y fecha-hasta requeridos'},400
        
class TodosLosExperimentos(Resource):
    def get(self):
        return CommonService.jsonMany( ExperimentoService.experimentos(),ExperimentoSchema)
