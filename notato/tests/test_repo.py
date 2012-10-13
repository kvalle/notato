import unittest
from notato.models import Note
from notato.tests.base import NotatoTestCase

class MongoRepoTests(unittest.TestCase, NotatoTestCase):

    def setUp(self):
        self.commonSetUp()

    def test_save_note(self):
        note = Note(1)
        self.repo.save(note)
        ids = self.repo.get_ids()
        assert note.id in ids
        assert 1 == len(ids)
        
    def test_get_ids(self):
        ids = range(1,4)
        for i in ids:
            self.repo.save(Note(i))
        assert ids == self.repo.get_ids()
    
    def test_get_public_ids(self):
        self.repo.save(Note(1, public=True))
        self.repo.save(Note(2, public=False))
        self.repo.save(Note(3, public=True))
        ids = self.repo.get_public_ids()
        assert 1 in ids
        assert 2 not in ids
        assert 3 in ids

    def test_save_multiple_notes(self):
        new_ids = range(1,4)
        for i in new_ids:
            note = Note(i)
            self.repo.save(note)
        ids = self.repo.get_ids()
        assert new_ids == ids
        
    def test_delete_note(self):
        note = Note(1)
        self.repo.save(note)
        assert 1 == len(self.repo.get_ids())
        self.repo.delete(note.id)
        assert 0 == len(self.repo.get_ids())
        
    def test_get_note(self):
        note = Note(1,'my special note')
        self.repo.save(note)
        stored = self.repo.get(note.id)
        assert note.id == stored.id
        assert note.title == stored.title
        
if __name__ == '__main__':
    unittest.main()

