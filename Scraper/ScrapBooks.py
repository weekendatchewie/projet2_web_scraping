import requests
from bs4 import BeautifulSoup

from Category.Category import Category
from Book.Book import Book

main_page = "http://books.toscrape.com/"


# Get the url of the website then analyse its html
def get_url_request(url_req):
    url_request = requests.get(url_req)
    soup = BeautifulSoup(url_request.content, 'html.parser')
    return soup


class ScrapBooks:

    def __init__(self):
        self.list_categories = []

    def get_all_categories(self):
        soup = get_url_request(main_page)
        # Get the "ul" in the navbar
        get_first_ul = soup.find('ul', {"class": "nav-list"})
        # The "ul" wich contains the list of categories
        get_ul = get_first_ul.find('ul')
        # The "li" to get all the links the create the category
        list_books_category = get_ul.find_all('li')
        for li in list_books_category:
            category_name_in_link = li.find('a')['href'].split('/')[3]
            category = Category(category_name_in_link)
            self.list_categories.append(category)

    def get_all_books(self):
        for category in self.list_categories:
            soup = get_url_request("https://books.toscrape.com/catalogue/category/books/" + category.name + "/index.html")
            page = (soup.find("li", {"class": "current"}))
            # Check if there is no other pages for the category
            if page is None:
                all_h3 = soup.find_all('h3')
                for h3 in all_h3:
                    link_to_books = h3.select('a')
                    for a in link_to_books:
                        link_to_book = a['href'].strip('../../../')
                        url_book = main_page + 'catalogue/' + link_to_book
                        category.add_book(self.get_book_infos(url_book))
            else:
                page = str(page)
                page = page.split()[5]
                nb_pages = int(page)
                for i in range(nb_pages + 1):
                    url = "https://books.toscrape.com/catalogue/category/books/" + category.name + "/page-" + str(
                        i) + ".html"
                    response = requests.get(url)
                    if response.ok:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        all_h3 = soup.find_all('h3')
                        for h3 in all_h3:
                            link_to_books = h3.select('a')
                            for a in link_to_books:
                                link_to_book = a['href'].strip('../../../')
                                url_book = main_page + 'catalogue/' + link_to_book
                                category.add_book(self.get_book_infos(url_book))

    def get_book_infos(self, url_book):
        soup = get_url_request(url_book)

        # Get the book title
        title_book = soup.find('h1').text

        # Get the category of the book
        ul_category = soup.select('ul.breadcrumb')
        for element in ul_category:
            category_book = element.select('li')[2].text.strip()

        # Get the image of the book
        image_book = soup.select('img')[0]
        # Change the path to get the good link
        image_src = main_page + image_book.get('src').strip('../../')

        # Get the product description
        product_description = soup.select('article > p')[0].text

        # Get the review rating, number of stars
        review_rating = soup.find('p', class_='star-rating').get('class')[1] + ' stars'

        # Get the informations of the book
        product_info = soup.select('table.table')
        for info in product_info:
            universal_product_code = info.select('tr > td')[0].text
            price_no_tax = info.select('tr > td')[2].text
            price_with_tax = info.select('tr > td')[3].text
            availabity_book = info.select('tr > td')[5].text

        book_details = Book(title_book, category_book, product_description, universal_product_code,
                            price_with_tax, price_no_tax, availabity_book, review_rating, url_book, image_src)

        return book_details

    def create_csv_books(self):
        for category in self.list_categories:
            category.create_csv()

    def download_images_books(self):
        for category in self.list_categories:
            category.download_images()
