import requests
from bs4 import BeautifulSoup
import csv


def book_product_detail(url):

    # Get the url of the website then analyse its html
    page_url = url
    url = requests.get(page_url)
    soup = BeautifulSoup(url.content, 'html.parser')


    # Get the book title
    title_book = soup.find('h1').text


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


    #print(title_book, '\n', category_book, '\n', image_src, '\n', product_description, '\n', upc_book, '\n', price_no_tax, '\n', price_with_tax, '\n', availabity_book, '\n', number_review)

    all_info_book = {}
    all_info_book['title'] = title_book
    all_info_book['category'] = category_book
    all_info_book['image'] = image_src
    all_info_book['description'] = product_description
    all_info_book['upc_book'] = upc_book
    all_info_book['price_no_tax'] = price_no_tax
    all_info_book['price_with_tax'] = price_with_tax
    all_info_book['availabity_book'] = availabity_book
    all_info_book['number_review'] = number_review

    info_book_header = ['title', 'category', 'image', 'description', 'upc_book', 'price_no_tax', 'price_with_tax', 'availabity_book', 'number_review']

    # with open('book_info.csv', 'w') as csvfile:
    #     fieldnames = list(all_info_book.keys())
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerow(all_info_book)
    print(all_info_book)


book_product_detail('http://books.toscrape.com/catalogue/the-mysterious-affair-at-styles-hercule-poirot-1_452/index.html')

