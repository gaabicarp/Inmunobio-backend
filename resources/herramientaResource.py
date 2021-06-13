from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError
from servicios.herramientaService import HerramientaService
from schemas.herramientaSchema import HerramientaSchema
from schemas.blogSchema import BlogSchema
from marshmallow import ValidationError
from servicios.commonService import CommonService
from exceptions.exception import ErrorBlogInexistente,ErrorHerramientaInexistente,ErrorFechasInvalidas

class HerramientaResource(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                HerramientaService.nuevaHerramienta(datos)
                return {'Status':'ok'},200  
            except ValidationError as err:
                return {'error': err.messages},400
        return {'name': 'None'},400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                HerramientaService.modificarHerramienta(datos)
                return {'Status':'ok'},200              
            except ValidationError as err:
                return {'error': err.messages},40
            except ErrorHerramientaInexistente as err:
                return {'error': err.message},400                
        return {'name': 'None'},400 
       
class HerramientaPorId(Resource):
    def get(self,id_herramienta):
        if(id_herramienta):
            try:
                herramienta = HerramientaService.find_by_id(id_herramienta)
                return CommonService.json(herramienta,HerramientaSchema)
            except ErrorHerramientaInexistente as err:
                return {'error': err.message},400     
        return {'error': 'Debe indicarse id_herramienta'},400

    def delete(self,id_herramienta):
        if(id_herramienta):
            try:
                HerramientaService.eliminarHerramienta(id_herramienta)
                return {'Status':'ok'},200              
            except ValidationError as err:
                return {'error': err.messages},400   
        return {'error': 'Debe indicarse id_herramienta'},400

class Herramientas(Resource):
     def get(self):
        herramienta =  HerramientaService.obtenerHerramientas()
        return CommonService.jsonMany(herramienta,HerramientaSchema)

class CrearBlogHerramientas(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                HerramientaService.nuevoBlogHerramienta(datos)
                return {'Status':'ok'},200              
            except ValidationError as err:
                return {'error': err.messages},40
            except ErrorHerramientaInexistente as err:
                return {'error': err.message},400                
        return {'name': 'None'},400 

class BlogHerramientaXId(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                blogs = HerramientaService.blogHerramienta(datos)
                return CommonService.jsonMany(blogs,BlogSchema)     
            except ValidationError as err:
                return {'error': err.messages},400
            except (ErrorHerramientaInexistente,ErrorFechasInvalidas) as err:
                return {'error': err.message},400 
        return {'Error': 'Parametros requeridos'},400  

class BorrarBlogHeramienta(Resource): 
    def delete(self,id_herramienta,id_blog):
        if(id_herramienta and id_blog):
            try:
                blogs = HerramientaService.borrarlogHerramienta(id_herramienta,id_blog)
                return {'Status':'ok'},200              
            except (ErrorHerramientaInexistente,ErrorBlogInexistente) as err:
                return {'error': err.message},400
        return {'name': 'None'},400 
                     



