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
        
    def test_login_redirects_properly(self):
        self.repo.save(Note(10))
        response = self.app.get('/notes/edit/10', follow_redirects=True)
        assert "You must log in" in response.data
        self.login()
        response = self.app.get('/notes/edit/10')
        assert "<h1>Edit note</h1>" in response.data

if __name__ == '__main__':
    unittest.main()
