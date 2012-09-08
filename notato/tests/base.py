from notato import app, repo
import hashlib

class NotatoTestCase():

    def commonSetUp(self):
        self.username = 'admin'
        self.password = 'password'
        app.config['TESTING'] = True
        app.config['USERNAME'] = self.username
        app.config['PASSWORD'] = hashlib.sha1(self.password).hexdigest()
        app.config['DATABASE'] = 'notato_test'
        self.app = app.test_client()
        self.repo = repo.MongoRepo('notato_test')

    def login(self):
        data = dict(username=self.username, password=self.password)
        return self.app.post('/log-in', data=data)

