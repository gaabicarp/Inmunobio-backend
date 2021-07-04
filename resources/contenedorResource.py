from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from servicios.contenedorService import ContenedorService

class Contenedor(Resource):

    #@jwt_required()
    def get(self):
        try:
            contenedores = ContenedorService.find_all()
            return contenedores, 200
        except ValidationError as err:
            return {'error': err.messages}, 400
        except Exception as err:
            return {'Error': str(err)}, 400

    #@jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                ContenedorService.nuevoContenedor(datos)
                return {'Status' : 'ok'}, 200
            except ValidationError as err:
                return {'error': err.messages},400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'error': 'Se deben enviar datos para la creación del contenedor'},400
    
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ContenedorService.modificarContenedor(datos)
                return {"Status": "Ok"}, 200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': "Se deben enviar datos para la modificación del contenedor."},400
    
    def delete(self, idContenedor):
        if idContenedor:
            try:
                ContenedorService.eliminarContenedor(idContenedor)
                return {"Status" : "Ok"}, 200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': "Se debe enviar el id del contenedor."},400

class ContenedorProyecto(Resource):
    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                contenedores = ContenedorService.asignarProyectoAlContenedor(datos)
                return {'Status': 'Ok'}, 200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': 'Se debe enviar un atributo id_proyecto válido'}, 400

class ContenedorProyectoId(Resource):
    #@jwt_required()
    def get(self,id_proyecto):
        if id_proyecto:
            try:
                contenedores = ContenedorService.find_all_by_id_proyecto(id_proyecto)
                return contenedores, 200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': 'Se debe enviar un atributo id_proyecto válido'}, 400

class ContenedorEspFisicoID(Resource):
    #@jwt_required()
    def get(self,id_espacioFisico):
        if id_espacioFisico:
            try:
                contenedores = ContenedorService.find_all_by_id_esp(id_espacioFisico)
                return contenedores,200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': 'Se debe enviar un atributo id_espacioFisico válido'}, 400

class ContenedorParent(Resource):
    #@jwt_required()
    def get(self):
        datos = request.get_json()
        if datos:
            try:
                contenedores = ContenedorService.subContenedoresDelContenedor(datos)
                return contenedores, 200
            except ValidationError as err:
                return {'Error': err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': 'Se debe enviar el id del contenedor'}, 400

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            try:
                ContenedorService.asignarParents(datos)
                return {'Status':'Ok'}
            except ValidationError as err:
                return {'Error' : err.messages}, 400
            except Exception as err:
                return {'Error': str(err)}, 400
        return {'Error': 'Se debe enviar el id del contenedor y el parent'}
