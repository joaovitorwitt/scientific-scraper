from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random


# RANDOM WALK - having an initial url parameter then in that page get a random link and go to this randoms link page, doing this recursively

random.seed(datetime.datetime.now().timestamp())
def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org{}'.format(articleUrl))
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'id': 'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))


links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)


# RECURSIVELY CRAWLING AN ENTIRE WEBSITE



