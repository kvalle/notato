import unittest
from notato import app
from notato import repo
from notato.models import Note
import hashlib
from flask import g

class EditNoteTests(unittest.TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = 'password'
        app.config['TESTING'] = True
        app.config['USERNAME'] = self.username
        app.config['PASSWORD'] = hashlib.sha1(self.password).hexdigest()
        app.config['DATABASE'] = 'notato_test'
        self.app = app.test_client()
        self.repo = repo.MongoRepo()
        self.repo.clear_all()
        self.login()
        
    def test_get_edit_page(self):
        self.repo.save(Note(1))
        response = self.app.get('/notes/edit/1')
        assert "<h1>Edit note</h1>" in response.data
        
    def test_get_edit_page_with_bad_id(self):
        response = self.app.get('/notes/edit/-1')
        assert 404 == response.status_code

    def test_post_to_save_note(self):
        data = dict(target_state='edit')
        response = self.app.post('/notes/edit/1', follow_redirects=True)
        assert "<h1>Edit note</h1>" in response.data

    def test_post_to_save_and_view_note(self):
        data = dict(target_state="read", note_title="my title")
        response = self.app.post('/notes/edit/1', data=data, follow_redirects=True)
        title = self.repo.get_title_by_id(1).encode('ascii')
        assert "<h1>%s</h1>" % title in response.data
    
    def login(self):
        data = dict(username=self.username, password=self.password)
        return self.app.post('/log-in', data=data)

if __name__ == '__main__':
    unittest.main()
