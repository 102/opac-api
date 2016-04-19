import unittest
from opacwrapper import OPACWrapper
from web import app

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

    def test_one_book(self):
        total, books = opac.get_book_list_by_author('Пушкин', length=1)
        self.assertEqual(len(books), 1)

    def test_offset_order(self):
        total1, books1 = opac.get_book_list_by_author('Smith', length=7, offset=0)
        total2, books2 = opac.get_book_list_by_author('Smith', length=7, offset=3)
        self.assertEqual(books1[3:], books2[:4])

    def test_web(self):
        with app.test_client() as c:
            resp = c.get('/?author=Smith&length=1&offset=1')
            self.assertGreater(len(resp.data), 0)

if __name__ == '__main__':
    unittest.main()
