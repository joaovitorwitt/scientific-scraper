from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime
import random


def get_book_titles():
    html = urlopen('https://books.toscrape.com/')
    bs = BeautifulSoup(html, 'html.parser')
    book_list = bs.find('ol', {'class': 'row'}).find_all('article', {'class': 'product_pod'})
    for book in book_list:
        
        print(book.find('h3').get_text())

get_book_titles()