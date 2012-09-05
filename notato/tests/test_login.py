import unittest
from notato import app
import hashlib

class NotatoTestCase(unittest.TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = 'password'
        app.config['TESTING'] = True
        app.config['USERNAME'] = self.username
        app.config['PASSWORD'] = hashlib.sha1(self.password).hexdigest()
        self.app = app.test_client()

    def test_login_required(self):
        response = self.app.get('/', follow_redirects=True)
        assert '<h1>Log in</h1>' in response.data
        
    def test_login_works(self):
        self.login()
        response = self.app.get('/', follow_redirects=True)
        assert 'Log out' in response.data

    def login(self):
        data = dict(username=self.username, password=self.password)
        return self.app.post('/log-in', data=data, follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
