from flask import Flask
from flask_mongoalchemy import MongoAlchemy

app= Flask(__name__)
app.config["MONGOALCHEMY_DATABASE"]="Prueba"
db = MongoAlchemy(app)

class Usuarios(db.Document):
	nombre = db.StringField()
	mail = db.StringField()

@app.route("/")
def Prueba():
	nuevo = Usuarios(nombre="Emmanuel", mail="alcaraz.emmanuel@gmail.com")
	nuevo.save()

	usuario = Usuarios.query.filter(Usuarios.nombre == "Emmanuel").first()
	return usuario.mail
if __name__ == "__main__":
	app.run(debug="true")