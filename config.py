import os

SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
PWD = os.path.abspath(os.curdir)

DEBUG = True
MONGODB_DB = 'db_mongo_inmunobio'
MONGODB_HOST = 'localhost'
#cambiar a mongo para subir, localhost para local
MONGODB_PORT = 27017
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql://root:secret@0.0.0.0:33060/db_mysql_inmunobio'
#cambiar a mysql:33060 , o 0.0.0.0 para local n.n
UPLOAD_FOLDER = PWD + '/uploads/'

