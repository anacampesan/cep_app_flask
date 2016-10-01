from flask import Flask
import unittest

from app import app, db, Zipcode


class ZipcodeTest(unittest.TestCase):

    def setUp(self):
        """
        Creates new test database
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test_database.db'
        db.create_all()

    def tearDown(self):
        """
        Dumps the db
        """
        db.drop_all()

    @app.errorhandler(404)
    def internal_error(error):
        db.session.rollback()
        return 404

    def test_list(self):
        zipcode = Zipcode('14800210','Rua xxx','Araraquara','SP','Bairro')
        db.session.add(zipcode)
        db.session.commit()
        assert len(Zipcode.query.all()) == 1
        assert Zipcode.query.first().zip_code == '14800210'

if __name__ == '__main__':
    unittest.main()
