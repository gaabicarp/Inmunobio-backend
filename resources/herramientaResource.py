from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from servicios.herramientaService import HerramientaService
from schemas.herramientaSchema import HerramientaSchema
from schemas.blogSchema import BlogSchemaExtendido
from servicios.commonService import CommonService

class HerramientaResource(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                HerramientaService.nuevaHerramienta(datos)
                return {'Status':'Se creo la nueva herramienta'},200  
            except Exception as err:
                return {'Error': err.args},400
        return {'Error': 'Deben suministrarse los datos para el alta de herramienta'},400

    def put(self):
        datos = request.get_json()
        if datos:
            try:
                HerramientaService.modificarHerramienta(datos)
                return {'Status':'Se modifico la herramienta'},200              
            except Exception as err:
                return {'Error': err.args},400          
        return {'Error': 'Deben suministrarse los datos para la modificacion de la herramienta'},400
       
class HerramientaPorId(Resource):
    def get(self,id_herramienta):
        if(id_herramienta):
            try:
                return CommonService.json(HerramientaService.find_by_id(id_herramienta),HerramientaSchema)
            except Exception as err:
                return {'Error': err.args},400 
        return {'Error': 'Debe indicarse id_herramienta'},400

    def delete(self,id_herramienta):
        if(id_herramienta):
            try:
                HerramientaService.eliminarHerramienta(id_herramienta)
                return {'Status':'Se elimino la herramienta.'},200              
            except Exception as err:
                return {'Error': err.args},400  
        return {'error': 'Debe indicarse id_herramienta'},400

class Herramientas(Resource):
     def get(self):
        return CommonService.jsonMany(HerramientaService.obtenerHerramientas(),HerramientaSchema)

class CrearBlogHerramientas(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                HerramientaService.nuevoBlogHerramienta(datos)
                return {'Status':'Se creo el blog de herramienta'},200              
            except Exception as err:
                return {'Error': err.args},400                  
        return {'Error': 'Deben suministrarse datos para la creacion del blog'},400 

class BlogHerramientaXId(Resource):
    def post(self):
        datos = request.get_json()
        if datos:
            try:
                blogs = HerramientaService.blogHerramienta(datos)
                return CommonService.jsonMany(blogs,BlogSchemaExtendido)     
            except Exception as err:
                return {'Error': err.args},400    
        return {'Error': 'Parametros requeridos'},400  

class BorrarBlogHeramienta(Resource): 
    def delete(self,id_herramienta,id_blog):
        if(id_herramienta and id_blog):
            try:
                blogs = HerramientaService.borrarlogHerramienta(id_herramienta,id_blog)
                return {'Status':'Se borró blog de herramienta.'},200              
            except Exception as err:
                return {'Error': err.args},400    
        return {'Error': 'Debe enviarse el id de herramienta y blog.'},400 
                     



