from pymongo import Connection
from notato.models import Note

class MongoRepo():

    def __init__(self, database):
        con = Connection()
        self.mongo = con[database]
        
    def get_ids(self):
        return sorted([n['_id'] for n in self.mongo.notes.find({},{'id':1})])

    def get_public_ids(self):
        return sorted([n['_id'] for n in self.mongo.notes.find({'public': True},{'id':1})])

    def get_title_by_id(self, note_id):
        d = self.mongo.notes.find_one({'_id': note_id}, {'title':1})
        if not d:
            return None
        note = Note(note_id, title=d['title'])
        return note.title_or_placeholder

    def save(self, note):
        if not note.id:
            note.id = self.next_id()
        return self.mongo.notes.save(note.as_data())

    def get(self, note_id):
        d = self.mongo.notes.find_one({'_id': note_id})
        if not d:
            return None
        return Note.from_dict(d)

    def delete(self, note_id):
        self.mongo.notes.remove({'_id': note_id})

    def clear_all(self):
        self.mongo.notes.drop()
        
    def next_id(self):
        if not self.get_ids():
            return 1
        return max(self.get_ids()) + 1

