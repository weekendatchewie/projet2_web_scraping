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
            csvfile.write("title,category: \n")
            for book in self.books:
                csvfile.write(book.title + "," + book.category + '\n')
