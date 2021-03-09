import requests
from bs4 import BeautifulSoup


# Get the url of the website then analyse its html
page_url = "http://books.toscrape.com/"
url = requests.get(page_url)
soup = BeautifulSoup(url.content, 'html.parser')


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

    # return the list
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
        self.link = ''
        self.books = []
        # print(f"Le nom de la catégorie créée est : {name}")

    def __str__(self):
        return self.name

    def add_link(self, link):
        self.link = link
        # print(f"Le nom de la catégorie créée est : {self.name} et le lien est : {link}")

    def add_book(self, book):
        print("On ajoute le livre " + book.title + " à la catégorie " + self.name)
        self.books.append(book)


list_categories = []

for categoryName in get_names_categories(get_all_categories()):
    category = Category(categoryName)
    list_categories.append(category)

for i in range(len(get_links_categories(get_all_categories()))):
    list_categories[i].add_link('http://books.toscrape.com/' + get_links_categories(get_all_categories())[i])

"""

TEST scrap une page catégorie pour récupérer les liens des livres

"""

url_page = requests.get(list_categories[0].link)
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

print(url_links2)

"""

TEST créer classe Book

"""


class Book:

    def __init__(self, title, category, description, universal_product_code, price_including_tax, price_excluding_tax, number_available, review_rating, product_page_url, image_url):
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
        print(f"Le livre {title} est bien créé \n {category} \n {description} \n {universal_product_code} \n {price_including_tax} \n {price_excluding_tax} \n {number_available} \n {review_rating} \n {product_page_url} \n {image_url}")

    def __str__(self):
        return self.title


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

    book_test = Book(title_book, category_book, product_description, upc_book, price_with_tax, price_no_tax, availabity_book, number_review, url_cat, image_src)
