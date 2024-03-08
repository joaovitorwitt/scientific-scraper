from urllib.request import urlopen
from urllib.parse import urlparse
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

# pages = set()
# def getLinks(pageUrl):
#     global pages
#     html = urlopen('http://en.wikipedia.org{}'.format(pageUrl))
#     bs = BeautifulSoup(html, 'html.parser')
#     try:
#         print(bs.h1.get_text())
#         print(bs.find(id='mw-content-text').find_all('p')[0])
#         print(bs.find(id='ca-edit').find('span').find('a').attrs['href'])

#     except AttributeError:
#         print("This page is missing something. Continuing!")

#     for link in bs.find_all('a', href=re.compile('^(/wiki/)')):
#         if 'href' in link.attrs:
#             if link.attrs['href'] not in pages:
#                 # we have a new page
#                 newPage = link.attrs['href']
#                 print('-'*20)
#                 print(newPage)
#                 pages.add(newPage)
#                 getLinks(newPage)


# getLinks('')

# CRAWLING ACROSS THE INTERNET
pages = set()
# random.seed(datetime.datetime.now())

# retrieves a list of all internal links found on the page
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme, urlparse(includeUrl).netloc)

    internalLinks = []

    # find all links that begin with a "/"
    for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if (link.attrs['href'].startswith('/')):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    
    return internalLinks


# retrieves a list of all external links found on a page
def getExternalLinks(bs, excludeUrl):
    externalLinks = []

    # finds all links that start with 'http' or 'www' that
    # do not contain the current URL
    for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])

    return externalLinks


def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bs = BeautifulSoup(html, 'html.parser')

    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links, looking around the site for one")
        domain = '{}//{}'.format(urlparse(startingPage).scheme, urlparse(startingPage).netloc)
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]
    

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print('Random external link is: {}'.format(externalLink))
    followExternalOnly(externalLink)


followExternalOnly('http://oreilly.com')
