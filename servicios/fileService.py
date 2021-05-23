import gridfs 
#from app import app
import os
from config import UPLOAD_FOLDER

class FileService():
    @classmethod
    def upload(cls,datos):
        filename = datos.filename
        datos.save(os.path.join(UPLOAD_FOLDER, filename))
        #chequear si hubo errores
        return filename