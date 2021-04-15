from Scraper.ScrapBooks import ScrapBooks

if __name__ == '__main__':
    scraper = ScrapBooks()
    scraper.get_all_categories()
    scraper.get_all_books()
    scraper.download_images_books()
    scraper.create_csv_books()
