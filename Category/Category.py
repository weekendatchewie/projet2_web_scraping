import csv
import os
import re
import requests


class Category:

    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def create_csv(self):
        # create a folder to put the csv files into
        path = 'csv_files'
        if not os.path.exists(path):
            os.makedirs(path)

        with open(path + '/' + self.name + '_book_info.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            csvfile.write("title,category,description,universal_product_code,price_including_tax,price_excluding_tax,"
                          "number_available,review_rating,product_page_url,image_url: \n")
            for book in self.books:
                writer.writerow(
                    [book.title, book.category, book.description, book.universal_product_code, book.price_including_tax,
                     book.price_excluding_tax, book.number_available, book.review_rating, book.product_page_url,
                     book.image_url])

            print(f"le csv de {self.name} créé")

    def download_images(self):
        path = 'pictures'
        if not os.path.exists(path):
            os.makedirs(path)

        for book in self.books:
            # Regex to change the name of the picture
            title = re.sub('[^a-zA-Z0-9 \n]', '', book.title)

            with open(path + '/' + title + ".jpg", "wb") as file:
                response = requests.get(book.image_url)
                file.write(response.content)
