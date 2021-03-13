from flask import Flask
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
import config

app= Flask(__name__)
app.config.from_object(config)

dbMongo = MongoAlchemy(app)
db = SQLAlchemy(app)

class Usuarios(dbMongo.Document):
	nombre = dbMongo.StringField()
	mail = dbMongo.StringField()

@app.route("/")
def Prueba():
	nuevo = Usuarios(nombre="Emmanuel", mail="alcaraz.emmanuel@gmail.com")
	nuevo.save()

	usuario = Usuarios.query.filter(Usuarios.nombre == "Nadia").first()

	from mysql.usuario.prueba import Prueba
	p = Prueba.query.filter_by(id=1).first()
	return f"Mysql: {p.prueba} Mongo: {usuario.mail}"

if __name__ == "__main__":
    app.run(port=8080)