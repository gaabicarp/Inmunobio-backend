from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.espacioFisicoService import EspacioFisicoService
from servicios.commonService import CommonService
from schemas.espacioFisicoSchema import EspacioFisicoSchema
from schemas.blogSchema import BlogSchemaExtendido

class EspacioFisico(Resource):

    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                EspacioFisicoService.altaEspacioFisico(datos)
                return {'Status':'Se creó el espacio físico.'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Se necesitan datos para dar de alta el espacio físico.'},400

    def put(self):
        datos = request.get_json()
        if(datos): 
            try:           
                EspacioFisicoService.modificarEspacio(datos)
                return {'Status':'Se modificó el espacio físico.'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Deben enviarse los datos para la modificación del espacio físico.'},400

class EspacioFisicoID(Resource):
    def get(self,id_espacioFisico):
        if id_espacioFisico:
            try:
                return CommonService.json(EspacioFisicoService.find_by_id(id_espacioFisico),EspacioFisicoSchema)
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Debe enviarse el id del espacio físico.'},400


    def delete(self,id_espacioFisico):
        if(id_espacioFisico):
            try:
                EspacioFisicoService.borrarEspacio(id_espacioFisico)
                return {'Status':'Se borró el espacio físico.'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Debe enviarse el id del espacio físico.'},400

class CrearBlogEspacioFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                EspacioFisicoService.crearBlogEspacioFisico(datos)
                return {'Status':'Se creó blog de espacio físico.'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Deben enviarse los datos para crear el blog de espacio físico.'},400

class BorrarBlogEspacioFisico(Resource):
    def delete(self,id_espacioFisico,id_blog):
        if id_espacioFisico and id_blog:
            try:
                EspacioFisicoService().BorrarBlogEspacioFisico(id_espacioFisico,id_blog)
                return {'Status':'Se borró el blog.'},200
            except Exception as err:
                return {'Error': err.args}, 400
        return {'Error': 'Debe enviarse el id de espacio físico y blog para borrar el blog.'},400

class ObtenerBlogsEspFisico(Resource):
    def post(self):
        datos = request.get_json()
        if(datos):
            try:
                return CommonService.jsonMany(EspacioFisicoService.obtenerBlogs(datos),BlogSchemaExtendido)
            except Exception as err:
                return {'Error': err.args}, 400           
        return {'Error': 'Deben enviarse los datos para obtener el blog de espacio físico.'},400

class EspaciosFisicos(Resource):
    def get(self): 
        return CommonService.jsonMany(EspacioFisicoService.obtenerEspacios(),EspacioFisicoSchema)




