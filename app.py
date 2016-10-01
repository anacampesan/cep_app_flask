from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from restless.fl import FlaskResource
from restless.preparers import FieldsPreparer
import requests
import logging
import json

# Flask app object
app = Flask(__name__)
# Database relative path (three slashes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./zipcode_database.db'
# DB object tied to app
db = SQLAlchemy(app)

# Postmon API GET url
POSTMON_URL = 'http://api.postmon.com.br/v1/cep/'

# Logging
LOG_FILE = 'zipcode_app.log'
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

# CEP model
class Zipcode(db.Model):
    zip_code        = db.Column(db.String(10), primary_key=True)
    address = db.Column(db.String(50))
    neighbourhood     = db.Column(db.String(50))
    city     = db.Column(db.String(50))
    state     = db.Column(db.String(50))

    def __init__(self, zip_code, address, neighbourhood, city, state):
        self.zip_code        = zip_code
        self.address = address
        self.neighbourhood     = neighbourhood
        self.city     = city
        self.state     = state

    def __repr__(self):
        return '<CEP %r>' % self.zip_code

# Restless CEP resource
class ZipcodeResource(FlaskResource):
    # Fields to be exposed to the client
    preparer = FieldsPreparer(fields={
        'zip_code'        : 'zip_code',
        'address' : 'address',
        'neighbourhood'     : 'neighbourhood',
        'city'     : 'city',
        'state'     : 'state'
    })

    # Lets the users make requests without authentication (auth not needed for this app)
    def is_authenticated(self):
        return True

    # GET
    def list(self):
        return Zipcode.query.all()

    # GET specific
    def detail(self, pk):
        return get_entry(pk)

    # POST
    # Makes a get request to Postmon and raises an error if the zipcode does not exist
    def create(self):
        req = requests.get(POSTMON_URL+self.data['zip_code'])
        if (req.status_code != 200):
            raise ValueError('Please provide a valid zipcode.')
        req = json.loads(req.text)
        entry = Zipcode(req['cep'], req['logradouro'], req['bairro'], req['cidade'], req['estado'])
        db.session.add(entry)
        return db.session.commit()

    # DELETE
    def delete(self, pk):
        db.session.delete(get_entry(pk))
        db.session.commit()

# Restless URLs Routes
ZipcodeResource.add_url_rules(app, rule_prefix='/api/zipcode/')

# Helper method that grabs an instance from the database
def get_entry(pk):
    return Zipcode.query.filter_by(zip_code=pk).first()
