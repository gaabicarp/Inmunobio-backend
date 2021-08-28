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

#app.config ['JSON_SORT_KEYS'] = True #prueba para respetar orden de json como viene

with app.app_context():
    db.create_all()
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
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def Prueba():
	from models.mysql.usuario import Usuario, Permiso
	from servicios.usuarioService import UsuarioService
	u = UsuarioService.find_by_email('naye')
	p = Permiso.query.limit(5).all()
	f = UsuarioService.findUsuariosHabilitados()
	return f"{f}"

	
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