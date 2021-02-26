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
        # print(f"Le nom de la catégorie créée est : {name}")

    def __str__(self):
        return self.name

    def add_link(self, link):
        self.link = link
        # print(f"Le nom de la catégorie créée est : {self.name} et le lien est : {link}")


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
    url_links2.append(page_url + i)

"""

TEST créer classe Book

"""

