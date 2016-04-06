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
    author = request.args.get('author') or 'Smith'
    amount = request.args.get('amount') or '10'
    amount, books = opac.get_book_list_by_author(author, amount)

    return jsonify({'amount': amount, 'books': books})

if __name__ == '__main__':
    app.run(debug=True)