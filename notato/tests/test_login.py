import os
import unittest
import tempfile
from flask.ext import shelve
from notato import app
import hashlib

class NotatoTestCase(unittest.TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = 'password'
        app.config['SHELVE_FILENAME'] = "notato/storage/test.db"
        app.config['TESTING'] = True
        app.config['USERNAME'] = self.username
        app.config['PASSWORD'] = hashlib.sha1(self.password).hexdigest()
        self.app = app.test_client()

    def tearDown(self):
        db = app.config['SHELVE_FILENAME']
        if os.path.isfile(db):
            os.unlink(db)

    def test_empty_db(self):
        self.login()
        response = self.app.get('/', follow_redirects=True)
        assert 'There are no notes yet' in response.data

    def test_login_required(self):
        response = self.app.get('/', follow_redirects=True)
        assert '<h1>Log in</h1>' in response.data

    def login(self):
        data = dict(username=self.username, password=self.password)
        return self.app.post('/log-in', data=data, follow_redirects=True)

    def logout(self):
        return self.app.get('/log-out', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
