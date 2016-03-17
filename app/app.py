import urllib.request
import urllib.parse
import re
import xml.etree.ElementTree as ET

username = 'GUEST'
password = 'GUESTE'
typeaccess = 'PayAccess'

OPAC_INIT_URL = 'http://opac.omsklib.ru/cgiopac/opacg/opac.exe'
OPAC_DIRECT_URL = 'http://opac.omsklib.ru/cgiopac/opacg/direct.exe'

author_name = 'smith'

session_id = '-1'

params = urllib.parse.urlencode({'arg0': username, 'arg1': password, 'TypeAccess': typeaccess})
url = OPAC_INIT_URL + ('?%s' % params)
with urllib.request.urlopen(url) as f:
    response = f.read().decode('utf-8').split('\r\n')
    for line in response:
        if not line.find('numsean') == -1:
            session_id = re.findall(r'"([^"]*)"', line)[0]

data = urllib.parse.urlencode({'_errorXsl': '/opacg/html/common/xsl/error.xsl',
                               '_wait:6M': '_xsl:/opacg/html/search/xsl/search_results.xsl', '_version': '2.5.0',
                               '_service': 'STORAGE:opacfindd:FindView', 'outformList[0]/outform': 'SHOTFORM',
                               'outformList[1]/outform': 'LINEORD', 'length': '15',
                               'query/body': '(AU {0})'.format(author_name),
                               'query/open': "{NC:<span class='red_text'>}", 'query/close': '{NC:</span>}',
                               'userId': username, 'session': session_id, 'iddb': '2', 'level[0]': 'Full',
                               'level[1]': 'Retro'})
url = OPAC_DIRECT_URL
with urllib.request.urlopen(url, data=data.encode('UTF-8')) as f:
    response = f.read().decode('utf-8')
    books = []
    tree = ET.ElementTree(ET.fromstring(response))

    for element in tree.findall('.//entry'):
        if element.text is not None and not element.text.lower().find(author_name.lower()) == -1:
            books.append(element.text)

print(books)
