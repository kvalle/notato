from markdown import markdown

class Note:
    def __init__(self, note_id, title="", text="", markdown=True):
        self.id = note_id
        self.title = title
        self.text = text
        self.markdown = markdown
    
    @property
    def content(self):
        return markdown(self.text) if self.markdown else self.text
    
    @property
    def title_or_placeholder(self):
        return self.title if self.title else "untitled note %d" % self.id

    def as_data(self):
        return {'_id': self.id, 
                'title': self.title, 
                'text': self.text, 
                'markdown': self.markdown}

