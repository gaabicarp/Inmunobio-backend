from flask import Flask
import config
from flask_migrate import Migrate
from flask_jwt import JWT
from db import db, dbMongo
from security import authenticate, identity

from flask_cors import CORS, cross_origin

app= Flask(__name__,static_folder='uploads')
app.config.from_object(config)

############################db configuracion
db.init_app(app)

#app.config ['JSON_SORT_KEYS'] = True #prueba para respetar orden de json como viene

with app.app_context():
    db.create_all()
	
dbMongo.init_app(app)

Migrate(app, db, compare_type=True)

nojwt = JWT(app, authenticate, identity) 

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


############################ Api configuracion
from api import api
api.init_app(app)
############################

@app.route("/uploads/<rel_filename>")
def test_files(rel_filename):
	from flask import url_for,send_from_directory
	import os
	uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
	return send_from_directory(directory=uploads, filename= rel_filename)

app.config['JSON_SORT_KEYS'] = False

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