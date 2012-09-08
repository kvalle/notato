import unittest
from notato.models import Note

class NoteTests(unittest.TestCase):

    def setUp(self):
        self.note = Note(1, text="## foo")

    def test_view_markdown_note_content(self):
        self.note.markdown = True
        assert "<h2>foo</h2>" in self.note.content
        
    def test_view_plain_note_content(self):
        self.note.markdown = False
        assert "## foo" in self.note.content
        
    def test_title_placeholder(self):
        self.note.title = ""
        assert "untitled" in self.note.title_or_placeholder
        self.note.title = "a real title"
        assert "untitled" not in self.note.title_or_placeholder
        
if __name__ == '__main__':
    unittest.main()

