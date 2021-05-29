from models.mongo.muestra import Muestra, MuestraSchema
from dateutil import parser
import datetime

class MuestraService:

    @classmethod
    def find_by_id(cls, idMuestra):
        return Muestra.objects.filter(id_muestra=idMuestra).first()

    @classmethod
    def find_all_by_experimento(cls, idExperimento):
        muestras = Muestra.objects.filter(id_experimento=idExperimento).all()
        return MuestraSchema.dump(muestras, many=True)

    