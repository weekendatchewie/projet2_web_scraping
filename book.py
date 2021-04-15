class Book:

    def __init__(self, title, category, description, universal_product_code, price_including_tax, price_excluding_tax,
                 availabity_book, review_rating, product_page_url, image_url):
        self.title = title
        self.category = category
        self.description = description
        self.universal_product_code = universal_product_code
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = availabity_book
        self.review_rating = review_rating
        self.product_page_url = product_page_url
        self.image_url = image_url

    def __str__(self):
        return self.title
