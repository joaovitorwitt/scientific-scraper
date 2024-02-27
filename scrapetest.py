from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random


# RANDOM WALK - having an initial url parameter then in that page get a random link and go to this randoms link page, doing this recursively

# random.seed(datetime.datetime.now().timestamp())
# def getLinks(articleUrl):
#     html = urlopen('http://en.wikipedia.org{}'.format(articleUrl))
#     bs = BeautifulSoup(html, 'html.parser')
#     return bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))


# links = getLinks('/wiki/Kevin_Bacon')
# while len(links) > 0:
#     newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
#     print(newArticle)
#     links = getLinks(newArticle)


# RECURSIVELY CRAWLING AN ENTIRE WEBSITE

# pages = set()
# def getLinks(pageUrl):
#     global pages
#     html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
#     bs = BeautifulSoup(html, 'html.parser')
#     for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
#         if 'href' in link.attrs:
#             if link.attrs['href'] not in pages:
#                 # we have a new page
#                 newPage = link.attrs['href']
#                 print(newPage)
#                 pages.add(newPage)
#                 getLinks(newPage)


# getLinks('')


# COLLECTING DATA ACROSS THE ENTIRE SITE

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
    bs = BeautifulSoup(html, 'html.parser')
    try:
        print(bs.h1.get_text())
        print(bs.find(id='mw-content-text').find_all('p')[0])
        print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])

    except AttributeError:
        print("This page is missing something. Continuing!")

    for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # we have a new page
                newPage = link.attrs['href']
                print('-'*20)
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)


getLinks('')

