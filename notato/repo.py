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
        return [n['note_id'] for n in self.mongo.notes.find()]

    def insert(self, note):
        return self.mongo.notes.insert(note.as_data())

    def get(self, note_id):
        d = self.mongo.notes.find_one({'note_id':note_id})
        return Note(d['note_id'], d['title'], d['text'], d['markdown'])

    def delete(self, note_id):
        self.mongo.notes.remove({'note_id':note_id})

    def clear_all(self):
        self.mongo.notes.drop()

@app.before_request
def before_request():
    g.repo = MongoRepo()

def next_id():
    if not g.repo.get_ids():
        return 1
    return max(g.repo.get_ids()) + 1

