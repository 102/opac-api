from flask import Flask, request, make_response, send_from_directory
from opacwrapper import OPACWrapper
from json import dumps
from template import template

app = Flask(__name__)
opac = OPACWrapper()


def jsonify(data):
    data = dumps(data, ensure_ascii=False)
    response = make_response(data)
    response.headers['Content-Type'] = 'Application/json; charset=UTF-8'
    return response


@app.route('/')
def index():
    return template


@app.route('/api')
def api():
    author = 'au', request.args.get('author')
    title = 'ti', request.args.get('title')
    amount = request.args.get('amount') or '10'
    offset = request.args.get('offset') or '0'

    amount, books = opac.get_book_list(dict((author, title)), length=amount, offset=offset)

    response = {'amount_of_books_for_query': amount, 'amount_of_books_in_response': len(books), 'books': books}
    if not offset == '0':
        response['offset'] = offset

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
