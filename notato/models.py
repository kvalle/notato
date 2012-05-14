class Note:
    def __init__(self, note_id=None, title="", text="", markdown=True):
        self.id = note_id
        self.title = title
        self.text = text
        self.markdown = markdown

