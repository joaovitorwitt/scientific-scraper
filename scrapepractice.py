from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import datetime
import random
import requests
import json
        

def extract_book_information():
    json_objects = []

    current_page = 1
    while current_page != 6:
        url = f'https://books.toscrape.com/catalogue/page-{current_page}.html'
        response = requests.get(url)
        html = response.content

        bs = BeautifulSoup(html, 'html.parser')

        books = bs.find_all('article', {'class' : 'product_pod'})

        for book in books:
            book_element = book.find('h3').find('a')
            book_url = f'https://books.toscrape.com/catalogue/{book_element.attrs["href"]}'
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
                available_to_buy = True
            else:
                print('book not available')
                available_to_buy = False
                        
            print(book_url)

            print("="*40) # separator

            # data to be writed to a json file

            el = {
                'TITLE': book_title,
                'CATEGORY': actual_text,
                'PRICE': book_price,
                'RATING': actual_rating,
                'NUMBER OF REVIEWS': number_of_reviews,
                'BOOK INSTOCK': available_to_buy,
                'BOOK URL': book_url,
                'BOOK IMAGE URL': f'https://books.toscrape.com/{actual_book_url}'
            }
            json_objects.append(el)

        
        current_page = current_page + 1
    with open('sample.json', 'w') as file:
            json.dump(json_objects, file, indent=4)


extract_book_information()

    