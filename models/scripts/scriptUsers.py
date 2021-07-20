from flask import Flask
from app import db
from models.mysql.usuario import *
from flask import request
import io
import csv
app = Flask(__name__)

class SqlScriptUsuarios:
    def __init__(self):
        pass
    def llenarTablasUsuarios():
            import os
            with open(os.path.join('models/scripts/data/', 'asd.csv'), 'rb') as f:
                """spamreader = csv.reader(f, delimiter=' ', quotechar='|')
                for row in spamreader:
                    print (', '.join(row)) """
                stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
                csv_input = csv.reader(stream)
                print(csv_input)
                for row in csv_input:
                    print(row)
            return {'Status':'Usuarios ok'},200
       


