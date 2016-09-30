from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
current_dir = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./cep_database.db'
db = SQLAlchemy(app)

class Cep(db.Model):
    cep = db.Column(db.String(10), primary_key=True)
    # logradouro = db.Column(db.String(50))
    # bairro = db.Column(db.String(50))
    # cidade = db.Column(db.String(50))
    # estado = db.Column(db.String(50))

    def __init__(self, cep):
        self.cep = cep

    def __repr__(self):
        return '<CEP %r>' % self.cep
