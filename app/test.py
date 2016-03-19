import unittest
from app.opacwrapper import OPACWrapper

opac = OPACWrapper()


class TestOPACWrapper(unittest.TestCase):
    def test_cyrillic_author_name(self):
        total, books = opac.get_book_list_by_author('Пушкин', length=2)
        self.assertGreater(int(total), 0)

    def test_latin_author_name(self):
        total, books = opac.get_book_list_by_author('Smith', length=10)
        self.assertGreater(int(total), 0)

    def test_failed_name(self):
        total, books = opac.get_book_list_by_author('Failed_name')
        self.assertEqual(int(total), 0)

    def test_request_with_default_length(self):
        total, books = opac.get_book_list_by_author('Пушкин')
        self.assertEqual(len(books), opac.DEFAULT_LENGTH)

if __name__ == '__main__':
    unittest.main()
