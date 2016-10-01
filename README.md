# Zipcode Finder

This Flask webapp lets you make requests and grab information on zipcodes through the Postmon API and add it to a SQLite database using the SQLAlchemy ORM.

### Installation

Zipcode requires Python >= 2.7 to run, as well as pip so that the other libs can be installed. Then, the virtualenv has to be activate in order to avoid conflicts with dependencies. A FLASK_APP environment variable has to be set for Flask to know what app to run when ``flask run`` is entered. You're all set to start making requests!

```sh
source venv/Scripts/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```
