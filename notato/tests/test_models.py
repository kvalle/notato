import unittest
from notato.models import Note

class NoteTests(unittest.TestCase):

    def setUp(self):
        self.note = Note(1, text="## foo")

    def test_markdown_note_content(self):
        self.note.markdown = True
        assert "<h2>foo</h2>" in self.note.content
        
    def test_plain_note_content(self):
        self.note.markdown = False
        assert "## foo" in self.note.content
        
if __name__ == '__main__':
    unittest.main()
    


