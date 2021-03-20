from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

app= Flask(__name__)
app.config.from_object(config)

dbMongo = MongoAlchemy(app)
db = SQLAlchemy(app)
Migrate(app,db, compare_type=True)

from db_mysql.usuario.models.usuario import *

class Usuarios(dbMongo.Document):
	nombre = dbMongo.StringField()
	mail = dbMongo.StringField()

@app.route("/")
def Prueba():
	from db_mysql.usuario.models.usuario import Usuario, Permiso
	u = Usuario.query.limit(1).all()
	p = Permiso.query.limit(5).all()
	return f"{p}"

@app.route('/llenar_msyql')
def llenar_msyql():
	from db_mysql.usuario.models.sql_script import MysqlScript
	p = MysqlScript
	p.ScriptLlenarTablas()

if __name__ == "__main__":
    app.run(port=8080)