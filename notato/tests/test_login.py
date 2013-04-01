import unittest
from notato.tests.base import NotatoTestCase
from notato.models import Note

class LoginTests(unittest.TestCase, NotatoTestCase):

    def setUp(self):
        self.commonSetUp()

    def test_login_required(self):
        response = self.app.get('/', follow_redirects=True)
        assert '<h1>Log in</h1>' in response.data
        
    def test_login_works(self):
        self.login()
        response = self.app.get('/')
        assert 'Log out' in response.data

    def test_login_bad_username(self):
        response = self.login(user="invalid user")
        assert "Invalid username or password." in response.data

    def test_login_bad_password(self):
        response = self.login(password="invalid pwd")
        assert "Invalid username or password." in response.data
        
    def test_login_redirects_properly(self):
        self.repo.save(Note(10))
        response = self.app.get('/notes/edit/10', follow_redirects=True)
        assert "You must log in" in response.data
        
        response = self.login()
        assert response.status_code == 302
        assert response.location.endswith("/notes/edit/10")
        
    def test_logout(self):
        self.login()
        response = self.app.get('/log-out', follow_redirects=True)
        assert "You were logged out" in response.data
        response = self.app.get('/', follow_redirects=True)
        assert "You must log in" in response.data

if __name__ == '__main__':
    unittest.main()
