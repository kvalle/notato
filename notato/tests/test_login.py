import unittest
from notato.tests.base import NotatoTestCase

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

if __name__ == '__main__':
    unittest.main()
