from flask import Flask
import config
from models import *

app= Flask(__name__)
app.config.from_object(config)




############################ Api configuracion
from flask_restful import Resource, Api
from resources.usuarios import Usuarios
from resources.usuariosXUsername import UsuarioxUsername

api = Api(app)
api.add_resource(Usuarios, '/api/usuarios')
api.add_resource(UsuarioxUsername, '/api/usuario/<string:username>')

############################



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