from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime
import random


# challenges 1 and 2 
def extract_book_title_price_rating():
    # get desired url to scrape
    html = urlopen("https://books.toscrape.com/")

    # initialize beautiful soup object
    bs = BeautifulSoup(html, 'html.parser')

    wrapper_content = bs.find("ol", {"class" : "row"})

    for book in wrapper_content.find_all('article', {'class': 'product_pod'}):
        title = book.find('h3').text
        price = book.find('div', {'class': 'product_price'}).find('p', {'class': "price_color"}).get_text()

        # extract book rating
        rating_classes = book.find('p', {'class': 'star-rating'})['class']
        rating = [r for r in rating_classes if r != 'star-rating'][0]

        match rating:
            case "One":
                rating = '1/5'
            case "Two":
                rating = '2/5'
            case "Three":
                rating = '3/5'
            case "Four":
                rating = '4/5'
            case "Five":
                rating = '5/5'

        book_urls = book.find_all('a', href=re.compile("^catalogue.*index\.html$"))

        for book_url in book_urls:
            href_attribute = book_url.get('href')
        print(f'https://books.toscrape.com/{href_attribute}')

        # print book title
        print(title)
        # print book price
        print(price)
        print("Rating: ", rating)
        # print(book_url)
        print("="*40) # this print statement is just for separation
        

extract_book_title_price_rating()