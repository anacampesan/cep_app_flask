from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from restless.fl import FlaskResource
from restless.preparers import FieldsPreparer

app = Flask(__name__)
# Database relative path (three slashes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./cep_database.db'
db = SQLAlchemy(app)

# Model
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

# Restless resource
class CepResource(FlaskResource):
    preparer = FieldsPreparer(fields={
        'cep': 'cep'
    })

    # GET
    def list(self):
        return Cep.query.all()

    # GET specific
    def detail(self, pk):
        return Cep.query.filter_by(cep=pk).first()

# URLs Routes
CepResource.add_url_rules(app, rule_prefix='/cep/')
