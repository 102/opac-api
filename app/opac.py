from opacwrapper import OPACWrapper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--author', required=True)
parser.add_argument('-m', '--amount', help='Amount of books in result', default='10')
args = parser.parse_args()

opac = OPACWrapper()
amount, books = opac.get_book_list_by_author(args.author, args.amount)
print('Total amount of books:', amount)
print('-------------------------')
counter = 1
for book in books:
    print('{0}: {1}'.format(counter, book))
    counter += 1
