import os.path
import config

def list_ids():
    return sorted(map(int, os.listdir(config.STORAGE)))

def write(note_id, text):
    with open(_note_file_name(note_id), 'w') as n:
        n.write(text)
        
def _note_file_name(note_id):
    return os.path.join(config.STORAGE, str(note_id))

def read(note_id):
    if not _is_note(note_id):
        return ""
    with open(_note_file_name(note_id), 'r') as n:
        return n.read()

def _is_note(note_id):
    return os.path.isfile(_note_file_name(note_id))

