from flask import Flask, request, make_response
from opacwrapper import OPACWrapper
from json import dumps

app = Flask(__name__)
opac = OPACWrapper()


def jsonify(data):
    data = dumps(data, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'Application/json; charset=UTF-8'
    return response


@app.route('/')
def index():
    author = 'au', request.args.get('author')
    title = 'ti', request.args.get('title')
    amount = request.args.get('amount') or '10'
    offset = request.args.get('offset') or '0'

    amount, books = opac.get_book_list(dict((author, title)), length=amount, offset=offset)

    return jsonify({'amount_of_books_for_query': amount, 'amount_of_books_in_response': len(books), 'books': books})

if __name__ == '__main__':
    app.run(debug=True)