from markdown import markdown

class Note:
    def __init__(self, note_id=None, title="", text="", markdown=False, public=False):
        self.id = note_id
        self.title = title
        self.text = text
        self.markdown = markdown
        self.public = public
    
    @property
    def content(self):
        return markdown(self.text) if self.markdown else self.text
    
    @property
    def title_or_placeholder(self):
        if self.title:
            return self.title 
        if self.id:
            return "untitled note %d" % self.id
        return "untitled note"

    def as_data(self):
        return {'_id': self.id, 
                'title': self.title, 
                'text': self.text, 
                'markdown': self.markdown,
                'public': self.public}
    
    @staticmethod
    def from_dict(d):
        note = Note(d['_id'])
        note.title = d.get('title', '')
        note.text = d.get('text', '')
        note.markdown = d.get('markdown', False)
        note.public = d.get('public', False)
        return note
