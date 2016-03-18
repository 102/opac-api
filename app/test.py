from app.opacwrapper import OPACWrapper

opac = OPACWrapper()
print(opac.get_book_list_by_author('Пушкин', length=2))
print(opac.get_book_list_by_author('Smith', length=10))