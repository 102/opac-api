import unittest
from opacwrapper import OPACWrapper
from web import app
import json

opac = OPACWrapper()


def parse_response(resp):
    response = resp.data.decode('UTF-8')
    parsed = json.loads(response)
    return parsed


class TestOPACWrapper(unittest.TestCase):
    def test_cyrillic_author_name(self):
        total, books = opac.get_book_list({'au': 'Пушкин'}, length=2)
        self.assertGreater(int(total), 0)

    def test_latin_author_name(self):
        total, books = opac.get_book_list({'au': 'Smith'}, length=10)
        self.assertGreater(int(total), 0)

    def test_failed_name(self):
        total, books = opac.get_book_list({'au': 'Failed_name'})
        self.assertEqual(int(total), 0)

    def test_request_with_default_length(self):
        total, books = opac.get_book_list({'au': 'Пушкин'})
        self.assertEqual(len(books), opac.DEFAULT_LENGTH)

    def test_one_book(self):
        total, books = opac.get_book_list({'au': 'Пушкин'}, length=1)
        self.assertEqual(len(books), 1)

    def test_offset_order(self):
        total1, books1 = opac.get_book_list({'au': 'Smith'}, length=7, offset=0)
        total2, books2 = opac.get_book_list({'au': 'Smith'}, length=7, offset=3)
        self.assertEqual(books1[3:], books2[:4])

    def test_request_with_title(self):
        total, books = opac.get_book_list({'ti': 'Smith'})
        self.assertGreater(len(books), 0)


class TestWebServer(unittest.TestCase):
    def test_web_author_query(self):
        with app.test_client() as c:
            resp = c.get('/?author=Smith&amount=3&offset=1')
            self.assertEqual(len(parse_response(resp)['books']), 3)

    def test_web_title_query(self):
        with app.test_client() as c:
            resp = c.get('/?title=Золотая+рыбка&amount=5&type=TI')
            total, books = opac.get_book_list({'ti': 'Золотая рыбка'}, length=5)
            self.assertGreater(len(resp.data), 0)
            self.assertEqual(total, parse_response(resp)['amount'])
            self.assertEqual(books, parse_response(resp)['books'])

    def test_web_author_title_query(self):
        with app.test_client() as c:
            resp = c.get('/?title=Руслан+и+людмила&author=Пушкин&amount=4')
            self.assertGreater(len(resp.data), 0)
            self.assertEqual(4, len(parse_response(resp)['books']))

if __name__ == '__main__':
    unittest.main()
