import unittest
from bson.objectid import ObjectId
from pymongo import Connection
from notato.models import Note
from notato import repo
from notato import app

class NotatoTestCase(unittest.TestCase):

    # get_ids():
    # insert(note):
    # get(note_id):
    # delete(note_id):
    # next_id():

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'notato_test'
        self.app = app.test_client()
        self.repo = repo.MongoRepo()
        self.repo.clear_all()

    def test_insert_note(self):
        _id = 1
        note = Note(_id,'foo','bar',False)
        self.repo.insert(note)
        ids = self.repo.get_ids()
        assert _id in ids
        print ids
        assert 1 == len(ids)
        
    def test_insert_multiple_notes(self):
        new_ids = [1,2,3,4]
        for i in new_ids:
            note = Note(i,'foo','bar',False)
            self.repo.insert(note)
        ids = self.repo.get_ids()
        assert new_ids == ids

if __name__ == '__main__':
    unittest.main()
    


