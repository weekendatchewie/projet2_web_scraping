import requests
from bs4 import BeautifulSoup
import csv


# Get the url of the website then analyse its html
page_url = "http://books.toscrape.com/"
url_request = requests.get(page_url)
soup = BeautifulSoup(url_request.content, 'html.parser')


def get_all_categories():
    # Get the "ul" wich contains the list of categories
    get_first_ul = soup.find('ul', {"class": "nav-list"})
    get_ul = get_first_ul.find('ul')

    # Get the "a" wich contains the names and links of categories
    a_link = get_ul.find_all('a')
    return a_link


def get_names_categories(a_link):
    # declare an empty list for the a
    a_list = []
    # loop through the "a" to get every names of the categories and put in the list
    for a in a_link:
        a_list.append(a.text.strip())

    return a_list


def get_links_categories(a_link):
    # declare an empty list for the links
    a_href_list = []
    # loop through the "a" to get every texts and links of the categories and put in the list
    for a in a_link:
        a_href = a['href']
        a_href_list.append(a_href)

    return a_href_list


class Category:

    def __init__(self, name):
        self.name = name
        self.link = []
        self.books = []
        # print(f"Le nom de la catégorie créée est : {name}")

    def add_link(self, link):
        self.link = link
        print(f"Le nom de la catégorie créée est : {self.name} et le lien est : {link}")

    def add_book(self, book):
        print("On ajoute " + book.title + " à la catégorie " + self.name)
        self.books.append(book)

    def create_csv(self):
        with open(self.name + '_book_info.csv', 'w') as csvfile:
            csvfile.write("title,category,image: \n")
            for book in self.books:
                csvfile.write(book.title + "," + book.category + "," + book.image_url + '\n')
                # fieldnames = ['title', 'category']
                # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                # writer.writerow(book)

list_categories = []

for categoryName in get_names_categories(get_all_categories()):
    category = Category(categoryName)
    list_categories.append(category)

for i in range(len(get_links_categories(get_all_categories()))):
    list_categories[i].add_link('http://books.toscrape.com/' + get_links_categories(get_all_categories())[i])


class Book:

    def __init__(self, title, category, description, universal_product_code, price_including_tax, price_excluding_tax,
                 number_available, review_rating, product_page_url, image_url):
        self.title = title
        self.category = category
        self.description = description
        self.universal_product_code = universal_product_code
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.review_rating = review_rating
        self.product_page_url = product_page_url
        self.image_url = image_url
        # print(f"Le livre {title} est bien créé \n {category} \n {description} \n {universal_product_code} \n {price_including_tax} \n {price_excluding_tax} \n {number_available} \n {review_rating} \n {product_page_url} \n {image_url}")

    def __str__(self):
        return self.title


url_category = list_categories[0]
# for url_category in list_categories:

url_page = requests.get(url_category.link)
soup = BeautifulSoup(url_page.text, 'html.parser')
page_header = soup.select('div.page-header')[0].text.strip()

h3_list = []
a_href_list2 = []
all_h3 = soup.find_all('h3')
for h3 in all_h3:
    h3_list.append(h3)
    a_link2 = h3.select('a')
    for a in a_link2:
        a_href2 = a['href'].strip('../../../')
        a_href_list2.append(a_href2)

url_links2 = []

for i in a_href_list2:
    url_links2.append(page_url + 'catalogue/' + i)

"""
Test multi page
"""

try:
    get_next_page = soup.find('li', {"class": "next"})
    print(get_next_page)
    a_link_next = get_next_page.find('a')
    print(a_link_next)
    a_href_next = a_link_next['href']
    print(a_href_next)
    link_next_page = url_category.link.rstrip('index.html') + a_href_next
    print(link_next_page)
    url_category.add_link(link_next_page)
    list_categories.append(link_next_page)
except AttributeError:
    print('pas possible')

"""
*****
"""

for url_cat in url_links2:
    # Get the url of the website then analyse its html
    url = requests.get(url_cat)
    soup = BeautifulSoup(url.content, 'html.parser')

    # Get the book title
    title_book = soup.find('h1').text

    # Get the category of the book
    ul_category = soup.select('ul.breadcrumb')
    for element in ul_category:
        category_book = element.select('li')[2].text.strip()

    # Get the image of the book
    image_book = soup.select('img')[0]
    # Change the path to get the good link
    image_src = page_url + image_book.get('src').strip('../../')

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

    list_books = []
    book_test = Book(title_book, category_book, product_description, upc_book, price_with_tax, price_no_tax, availabity_book, number_review, url_cat, image_src)
    list_books.append(book_test)
    for b in list_books:
        url_category.add_book(b)
        url_category.create_csv()

    list_books = []

    # url_links2 = []
