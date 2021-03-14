from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

app= Flask(__name__)
app.config.from_object(config)

dbMongo = MongoAlchemy(app)
db = SQLAlchemy(app)
Migrate(app,db)

db.create_all()
db.session.commit()
from db_mysql.usuario.models.usuario import *

class Usuarios(dbMongo.Document):
	nombre = dbMongo.StringField()
	mail = dbMongo.StringField()

@app.route("/")
def Prueba():
	nuevo = Usuarios(nombre="Emmanuel", mail="alcaraz.emmanuel@gmail.com")
	nuevo.save()

	usuario = Usuarios.query.filter(Usuarios.nombre == "Nadia").first()

	from db_mysql.usuario.prueba import Prueba
	p = Prueba.query.filter_by(id=1).first()
	#compare_type=True

	return f"Mysql: {p.prueba} Mongo: {usuario.mail}"

if __name__ == "__main__":
    app.run(port=8080)