from models.mongo.proyecto import Proyecto, ProyectoSchema, ProyectoCerradoSchema, ProyectoModificarSchema
from flask_restful import Resource,Api
from flask_jwt import jwt_required
from flask import jsonify, request
from dateutil import parser
import json
from marshmallow import ValidationError
from pprint import pprint
class Proyectos(Resource):

    #@jwt_required()
    def get(self):
        proyectos = Proyecto.find_all()
        if proyectos:
           return proyectos 
        return {'name': 'None'},404

class NuevoProyecto(Resource):

    # @jwt_required()
    def post(self):
        datos = request.get_json()
        if datos:
            miembros = Proyecto.agregarMiembros()
            for miembro in miembros :
                print(miembro)
            schemaProyecto = ProyectoSchema()
            try:
                dictProyecto = schemaProyecto.load(datos)
                dictProyecto.save()
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},404
        return {'name': datos},404

class CerrarProyecto(Resource):

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            schemaProyecto = ProyectoCerradoSchema()
            try:
                dictProyecto = schemaProyecto.load(datos)
                Proyecto().cerrarProyecto(dictProyecto)
                return {'Status':'ok'},200
            except ValidationError as err:
                return {'error': err.messages},404
        return {'name': datos},404


class ProyectoID(Resource):

    #@jwt_required()
    def get(self):
        datos = request.get_json()
        if datos:
             proyecto = Proyecto.find_by_id(datos['id'])
             if proyecto:
                return proyecto.json(), 200
        return {'name': f"No se encontró ningún proyecto con el ID {datos['id']}"},400

class ModificarProyecto(Resource):

    #@jwt_required()
    def put(self):
        datos = request.get_json()
        if datos:
            proyectoSchema = ProyectoModificarSchema()
            try:
                dictProyecto = proyectoSchema.load(datos)
                Proyecto().modificarProyecto(dictProyecto)
                return {'Status':'ok'}, 200
            except ValidationError as err:
                return {'error': err.messages}, 404
        return {'name': datos}, 404
