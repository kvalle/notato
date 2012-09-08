import unittest
from notato.models import Note
from notato.tests.base import NotatoTestCase

class EditNoteTests(unittest.TestCase, NotatoTestCase):

    def setUp(self):
        self.commonSetUp()
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
        self.repo.save(Note(1))
        data = dict(target_state='edit')
        response = self.app.post('/notes/edit/1', follow_redirects=True)
        assert "<h1>Edit note</h1>" in response.data

    def test_post_to_save_and_view_note(self):
        self.repo.save(Note(1))
        data = dict(target_state="read", note_title="my title")
        response = self.app.post('/notes/edit/1', data=data, follow_redirects=True)
        title = self.repo.get_title_by_id(1).encode('ascii')
        assert "<h1>%s</h1>" % title in response.data
    
if __name__ == '__main__':
    unittest.main()
