class Note:
    def __init__(self, note_id, title="", text="", markdown=True):
        self.id = note_id
        self.title = title
        self.text = text
        self.markdown = markdown

    def as_data(self):
        return {'_id': self.id, 
                'title': self.title, 
                'text': self.text, 
                'markdown': self.markdown}
