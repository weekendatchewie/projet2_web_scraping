import requests
from bs4 import BeautifulSoup

# Get the url of the website then analyse its html

page_url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
url = requests.get(page_url)
soup = BeautifulSoup(url.text, 'html.parser')


# Get the book title
title_book = soup.select('h1')


# Get the category of the book
ul_category = soup.select('ul.breadcrumb')
for element in ul_category:
    category_book = element.select('li')[2].text.strip()


# Get the image of the book
image_book = soup.select('img')[0]
image_src = image_book.get('src')


# Get the product description
product_description = soup.select('article > p')[0].text


# Get the informations of the book
product_info = soup.select('table.table')
for info in product_info:
    upc_book = info. select('tr > td')[0].text
    price_no_tax = info. select('tr > td')[2].text
    price_with_tax = info. select('tr > td')[3].text
    availabity_book = info. select('tr > td')[5].text
    number_review = info. select('tr > td')[6].text
