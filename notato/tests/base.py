from notato import app, repo
import hashlib

class NotatoTestCase():

    def commonSetUp(self):
        self.username = 'admin'
        self.password = 'password'
        database = 'notato_test'
        app.config['TESTING'] = True
        app.config['USERNAME'] = self.username
        app.config['PASSWORD'] = hashlib.sha1(self.password).hexdigest()
        app.config['DATABASE'] = database
        self.app = app.test_client()
        self.repo = repo.MongoRepo(database)
        self.repo.clear_all()

    def login(self):
        data = dict(username=self.username, password=self.password)
        return self.app.post('/log-in', data=data)

