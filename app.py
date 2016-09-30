from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from restless.fl import FlaskResource
from restless.preparers import FieldsPreparer
import requests

# Flask app object
app = Flask(__name__)
# Database relative path (three slashes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./cep_database.db'
# DB object tied to app
db = SQLAlchemy(app)

POSTMON_URL = 'http://api.postmon.com.br/v1/cep/'

# CEP model
class Cep(db.Model):
    cep        = db.Column(db.String(10), primary_key=True)
    logradouro = db.Column(db.String(50))
    bairro     = db.Column(db.String(50))
    cidade     = db.Column(db.String(50))
    estado     = db.Column(db.String(50))

    def __init__(self, cep, logradouro, bairro, cidade, estado):
        self.cep        = cep
        self.logradouro = logradouro
        self.bairro     = bairro
        self.cidade     = cidade
        self.estado     = estado

    def __repr__(self):
        return '<CEP %r>' % self.cep

# Restless CEP resource
class CepResource(FlaskResource):
    preparer = FieldsPreparer(fields={
        'cep'        : 'cep',
        'logradouro' : 'logradouro',
        'bairro'     : 'bairro',
        'cidade'     : 'cidade',
        'estado'     : 'estado'
    })

    # Lets the users make requests without authentication (auth not needed for this app)
    def is_authenticated(self):
        return True

    # GET
    def list(self):
        return Cep.query.all()

    # GET specific
    def detail(self, pk):
        return Cep.query.filter_by(cep=pk).first()

    # POST
    def create(self):
        req = requests.get(POSTMON_URL, params=self.data['cep'])
        print(req.text)
        entry = Cep(req.text['cep'], req.text['logradouro'], req.text['bairro'], req.text['cidade'], req.text['estado'])
        db.session.add(entry)
        db.session.commit()

    # DELETE
    def delete(self, pk):
        entry = Cep.query.filter_by(cep=pk).first()
        db.session.delete(entry)
        db.session.commit()

# Restless URLs Routes
CepResource.add_url_rules(app, rule_prefix='/cep/')
