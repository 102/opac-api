from opacwrapper import OPACWrapper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--author', required=True)
parser.add_argument('-m', '--amount', help='Amount of books in result', default='10')
args = parser.parse_args()

opac = OPACWrapper()
print(opac.get_book_list_by_author(args.author, args.amount))
