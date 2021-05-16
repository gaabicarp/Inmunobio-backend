from flask_restful import Resource
from flask_jwt import jwt_required
from flask import request
from marshmallow import ValidationError

from servicios.fuenteExperimentalService import FuenteExperimentalService

class FuenteExperimental(Resource):

    def get(self, idFuenteExperimental):
        if idFuenteExperimental:
            fuenteExperimental = FuenteExperimentalService.find_by_id(idFuenteExperimental)
            if fuenteExperimental:
                return fuenteExperimental.json(), 200
            else:
                return {"Status" : f"No se encontró una fuente experimental para el id {idFuenteExperimental}"}, 200
        return {'Error': 'Es necesario indicar el id de la fuente experimental.'}, 400
