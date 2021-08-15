from flask import Flask
import config
from flask_migrate import Migrate
from flask_jwt import JWT
from db import db, dbMongo
#from api import api
from security import authenticate, identity
from flask_cors import CORS
from servicios.usuarioService import UsuarioService
app= Flask(__name__)
app.config.from_object(config)

#app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
############################db configuracion
db.init_app(app)

#db.create_all()
	#pass
	
dbMongo.init_app(app)

Migrate(app, db, compare_type=True)

nojwt = JWT(app, authenticate, identity) 

CORS(app)
cors = CORS(app,resources={r"/api/*":{"origins":"*"}})

############################ Api configuracion
from api import api
api.init_app(app)

############################

@app.route("/")
def Prueba():
	from models.mysql.usuario import Usuario, Permiso
	from servicios.usuarioService import UsuarioService
	u = UsuarioService.find_by_email('naye')
	p = Permiso.query.limit(5).all()
	f = UsuarioService.findUsuariosHabilitados()
	return f"{f}"

@app.route('/llenarUsuarios', methods=["POST"])
def llenar_usuarios():
	from models.scripts.scriptUsers import SqlScriptUsuarios
	return SqlScriptUsuarios.llenarTablasUsuarios()



#ejecutar esta funcion una unica vez para crear las tablas y los permisos
@app.route('/llenar_mysql')
def llenar_msyql():
	from models.scripts.sql_script import MysqlScript
	MysqlScript.ScriptLlenarTablas()
	return {'Status':'ok'}

@app.route('/prueba_csv')
def prueba_csv():
	from models.scripts.sql_script import MongoScript
	MongoScript().leerArchivoCSV('Proyecto.csv')
	return {'Status':'ok'}

	
if __name__ == "__main__":
	if app.config['DEBUG']:
		@app.before_first_request
		def create_tables():
			db.create_all()

	app.run(port=8080 ,debug=True)	

""" if __name__ == "__main__":
	db.init_app(app)
	dbMongo.init_app(app)
	if app.config['DEBUG']:
		@app.before_first_request
		def create_tables():
			db.create_all()
	Migrate(app,db,compare_type=True)
	app.run(port=8080) """