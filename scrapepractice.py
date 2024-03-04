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

        is_book_available = book.find('p', {'class': 'availability'})['class']
        
        next_page = requests.get(book_url)
        next_bs = BeautifulSoup(next_page.content, 'html.parser')

        category = next_bs.find("ul", {"class": "breadcrumb"}).find_all('li')[2:3]
        actual_category = ''.join(str(x) for x in category)
        match = re.search('<a\s+href="[^"]*">(.*?)<\/a>', actual_category)

        # book image URL
        book_image_url = next_bs.find('div', {'class': 'thumbnail'}).find('img')
        actual_book_url = book_image_url.attrs['src']
        print(f'https://books.toscrape.com/{actual_book_url}')

        # number of reviews
        number_of_reviews = next_bs.find('table', {'class': 'table-striped'}).find_all('tr')[-1].find('td').get_text()

        print(f'TITLE: {book_title}')

        if match:
            actual_text = match.group(1)
            print(f'CATEGORY: {actual_text}')
        else:
            print(actual_text)

        print(f'PRICE: {book_price}')
        print(f'RATING: {actual_rating}')
        print(f'NUMBER OF REVIEWS: {number_of_reviews}')
        if 'instock' in is_book_available:
            print('Book Instock')
        else:
            print('book not available')
                    
        print(book_url)

        print("="*40) # separator

        

extract_book_categories()