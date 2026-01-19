import unittest
from generator import extract_title


class TestGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = """
# My Title
This is some content.
"""
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    def test_extract_title_no_title(self):
        md = """
This is some content without a title.
"""
        with self.assertRaises(ValueError):
            extract_title(md)
