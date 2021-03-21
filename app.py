from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

from flask_restful import Resource, Api

app= Flask(__name__)
app.config.from_object(config)

dbMongo = MongoAlchemy(app)
db = SQLAlchemy(app)
Migrate(app,db, compare_type=True)

api = Api(app)

from db_mysql.usuario.models.usuario import *


class Usuarios(Resource):

    def get(self):
        usuarios = Usuario.query.limit(2).all()
        
        if usuarios:
            return [usuario.json() for usuario in usuarios]
        return {'name': 'None'},404

class UsuarioxUsername(Resource):

	def get(self, username):
		usuario = Usuario.query.filter_by(username = username).first()
		if usuario:
			return usuario.json()
		return {'name': 'None'},404


api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')

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