from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

#db = SQLAlchemy(), 
#Autoflush= false se agregó porque al instanciar al modelo de usuario
#pero no haber commiteado al usuario, este aparecia luego en las querys
#ya que también consulta sobre los cambios no commiteados
db = SQLAlchemy(session_options={"autoflush": False})
dbMongo = MongoEngine()
