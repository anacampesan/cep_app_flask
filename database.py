"""
By running this file, you can create the app's database file and populate it with some data.
You can also comment out the last 3 lines for database creation ONLY.
"""

from app import db, Cep
import requests

db.create_all()
