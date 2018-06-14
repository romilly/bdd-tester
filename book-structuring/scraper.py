from bs4 import BeautifulSoup
import re


def read(filename):
    with open(filename) as f:
        return f.read()

text = read('book-py.html')
soup = BeautifulSoup(text, 'html.parser')
print(soup.find_all(re.compile('h3|h4')))

