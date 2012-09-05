import unittest
from bson.objectid import ObjectId
from pymongo import Connection
from notato.models import Note
from notato import repo
from notato import app

class NotatoTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'notato_test'
        self.app = app.test_client()
        self.repo = repo.MongoRepo()
        self.repo.clear_all()

    def test_insert_note(self):
        note = Note(1)
        self.repo.insert(note)
        ids = self.repo.get_ids()
        assert note.id in ids
        assert 1 == len(ids)
        
    def test_get_ids(self):
        ids = range(3)
        for i in ids:
            self.repo.insert(Note(i))
        assert ids == self.repo.get_ids()
        
    def test_insert_multiple_notes(self):
        new_ids = range(4)
        for i in new_ids:
            note = Note(i)
            self.repo.insert(note)
        ids = self.repo.get_ids()
        assert new_ids == ids
        
    def test_delete_note(self):
        note = Note(1)
        self.repo.insert(note)
        assert 1 == len(self.repo.get_ids())
        self.repo.delete(note.id)
        assert 0 == len(self.repo.get_ids())
        
    def test_get_note(self):
        note = Note(1,'my special note')
        self.repo.insert(note)
        stored = self.repo.get(note.id)
        assert note.id == stored.id
        assert note.title == stored.title
        
if __name__ == '__main__':
    unittest.main()
    


