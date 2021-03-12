import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

r = requests.get(
    'http://socrates.vsau.org/wiki/index.php/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B0%D0%B4%D1%80%D0%B5%D1%81_%D0%B5%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D0%B8%D1%85_%D0%BF%D0%BE%D1%88%D1%82%D0%BE%D0%B2%D0%B8%D1%85_%D1%81%D0%BA%D1%80%D0%B8%D0%BD%D1%8C_%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%BD%D0%B8%D1%85_%D0%BF%D1%96%D0%B4%D1%80%D0%BE%D0%B7%D0%B4%D1%96%D0%BB%D1%96%D0%B2_%D1%83%D0%BD%D1%96%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%82%D0%B5%D1%82%D1%83')

html_text = r.text
body = BeautifulSoup(html_text, 'html.parser').body

pattern = re.compile(r'<p>(?P<institution>[А-ЯҐЄІЇа-яєії -]+)\s<b>(?P<email>[\w\.]+@[\w\.]+)')

matches = pattern.finditer(str(body))

results = []
for match in matches:
    institution = match.group('institution').strip()
    email = match.group('email')
    results.append((institution, email))

pprint(results)
