"""
By running this file, you can create the app's database file and populate it with some data.
You can also comment out the last 3 lines for database creation ONLY.
"""

from app import db, Cep
import requests

db.create_all()

req = requests.get('http://api.postmon.com.br/v1/cep/14800210')
entry = Cep('14800210', 'Rua Pedro Alvares Cabral', 'Jardim Artico', 'Araraquara', 'Sao Paulo')
db.session.add(entry)
db.session.commit()
