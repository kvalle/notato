from notato import app
from flask import g
from bson.objectid import ObjectId
from pymongo import Connection
from notato.models import Note

class MongoRepo():

    def __init__(self):
        con = Connection()
        self.mongo = con[app.config['DATABASE']]
        
    def get_ids(self):
        return [n['_id'] for n in self.mongo.notes.find()]
        
    def get_title_by_id(self, note_id):
        d = self.mongo.notes.find_one({'_id': note_id})
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
        return Note(d['_id'], d['title'], d['text'], d['markdown'])

    def delete(self, note_id):
        self.mongo.notes.remove({'_id': note_id})

    def clear_all(self):
        self.mongo.notes.drop()
        
    def next_id(self):
        if not self.get_ids():
            return 1
        return max(self.get_ids()) + 1

@app.before_request
def before_request():
    g.repo = MongoRepo()

def next_id():
    return g.repo.next_id()
