import urllib.request
import urllib.parse
import re
import xml.etree.ElementTree as ET
from app.util.xmltodict import XmlListConfig
from functools import reduce


class OPACWrapper(object):
    DEFAULT_LENGTH = 10

    username = 'GUEST'
    password = 'GUESTE'
    type_access = 'PayAccess'

    OPAC_INIT_URL = 'http://opac.omsklib.ru/cgiopac/opacg/opac.exe'
    OPAC_DIRECT_URL = 'http://opac.omsklib.ru/cgiopac/opacg/direct.exe'

    session_id = '-1'

    def __init__(self):
        """
        constructor used to get session_id from opac
        """
        params = urllib.parse.urlencode({'arg0': self.username, 'arg1': self.password, 'TypeAccess': self.type_access})
        url = self.OPAC_INIT_URL + ('?%s' % params)
        with urllib.request.urlopen(url) as f:
            response = f.read().decode('utf-8').split('\r\n')
            for line in response:
                if not line.find('numsean') == -1:
                    self.session_id = re.findall(r'"([^"]*)"', line)[0]

    def get_book_list_by_author(self, author_name, length=DEFAULT_LENGTH):
        """
        :param author_name: name of the author to be searched
        :param length: maximum length of returned books list
        :return: length, books: tuple, where first element is total amount of books, which can be found with this query
                                             second element is list of books
        """
        data = urllib.parse.urlencode({'_errorXsl': '/opacg/html/common/xsl/error.xsl',
                                       '_wait:6M': '_xsl:/opacg/html/search/xsl/search_results.xsl',
                                       '_version': '2.5.0', '_service': 'STORAGE:opacfindd:FindView',
                                       'outformList[0]/outform': 'SHOTFORM', 'outformList[1]/outform': 'LINEORD',
                                       'length': length, 'query/body': '(AU {0})'.format(author_name),
                                       'query/open': "{NC:<span class='red_text'>}", 'query/close': '{NC:</span>}',
                                       'userId': self.username, 'session': self.session_id, 'iddb': '2',
                                       'level[0]': 'Full', 'level[1]': 'Retro'})
        url = self.OPAC_DIRECT_URL
        with urllib.request.urlopen(url, data=data.encode('UTF-8')) as f:
            response = f.read().decode('utf-8')
            tree = ET.ElementTree(ET.fromstring(response))
            root = tree.getroot()
            size = reduce(lambda a, b: a + (b[1] if b[0] == 'size' else ''), root.items(), '')

            books = map(lambda i: i['SHOTFORM']['content']['entry'], XmlListConfig(root)[0]) if not size == '0' else []

            return size, list(books)
