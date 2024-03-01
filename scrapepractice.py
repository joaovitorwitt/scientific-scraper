from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime
import random
import requests

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
        

        next_page = requests.get(f'https://books.toscrape.com/{href_attribute}')
        next_bs = BeautifulSoup(next_page.content, 'html.parser')
        description = next_bs.find('article', {'class': 'product_page'}).find('p', {'class' : None}).get_text()

        # print book title
        print(title)

        # print book price
        print(price)

        print(description)
        
        print("Rating: ", rating)
        print(f'https://books.toscrape.com/{href_attribute}')
        print("="*40) # this print statement is just for separation
        

# extract_book_title_price_rating()
        

def extract_book_categories():
    html = urlopen("https://books.toscrape.com/")

    bs = BeautifulSoup(html, 'html.parser')

    # title, category, price, rating
    books = bs.find_all('article', {'class' : 'product_pod'})

    for book in books:
        book_element = book.find('h3').find('a',  href=re.compile("^catalogue.*index\.html$"))
        book_url = f'https://books.toscrape.com/{book_element.attrs["href"]}'
        book_title = book_element.attrs['title']
        book_price = book.find('div', {'class': 'product_price'}).find('p', {'class': 'price_color'}).get_text()

        book_rating = book.find('p', {'class': 'star-rating'})['class']

        for r in book_rating:
            if r != 'star-rating':
                actual_rating = r

        rating_dictionary = {
            "One": "1/5",
            "Two": "2/5",
            "Three": "3/5",
            "Four": "4/5",
            "Five": "5/5"
        }
        actual_rating = rating_dictionary.get(actual_rating, "wrong")

        print(actual_rating)
        

        # print(book_url)
        # print(f'TITLE: {book_title}')
        # print(f'PRICE: {book_price}')
        # print(book_rating)

        print("="*40) # separator

    # to get the category we also need to extract the URL
        

extract_book_categories()