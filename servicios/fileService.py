#from app import app
import os
from config import UPLOAD_FOLDER

class FileService():
    @classmethod
    def upload(cls,producto,datos):
        filename = f"{producto.id_producto}_{datos.filename}"
        datos.save(os.path.join(UPLOAD_FOLDER, filename))
        #chequear si hubo errores
        return filename
        
    @classmethod    
    def deleteFile(cls,filename):
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        


