import os
import requests
from bs4 import BeautifulSoup, Comment

packages_to_mirror = [
    'pytz',
    'python-dateutil',
    'six'
]

with open('index.html.template', 'r') as index:
    index_soup = BeautifulSoup(index, features='html.parser')

for package in sorted(packages_to_mirror):
    pypi_url = f'https://pypi.org/simple/{package}/'
    pypi_html = requests.get(pypi_url).content
    soup = BeautifulSoup(pypi_html, features='html.parser')
    soup.insert(1, Comment(\
        f'This file is replicated from {pypi_url}. Do not update directly as updates will be overridden when the page is update on PyPi.'))

    os.makedirs(package, exist_ok=True)

    with open(f'{package}/index.html', 'w+') as package_index:
        package_index.write(str(soup))

    index_entry = index_soup.find(name='a', string=package)

    if not index_entry:
        index_entry = index_soup.new_tag('a', href=f'/pypi-repo/{package}/')
        index_entry.string = package
        index_entry.append(index_soup.new_tag('br'))
        index_soup.html.body.append(index_entry)
        index_soup.html.body.append('\n')

index_soup.insert(1, Comment(\
    f'This file is generated via a script, so any manual updates will be overriden.'))

with open('index.html', 'w+') as index_html:
    index_html.write(str(index_soup))
