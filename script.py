import requests
from bs4 import BeautifulSoup

# Get the url of the website then analyse its html

page_url = "http://books.toscrape.com/"
url = requests.get(page_url)
soup = BeautifulSoup(url.text, 'html.parser')

# Get the "ul" wich contains the list of categories
# get_ul = soup.find('ul', {"class": "nav-list"})
get_ul = soup.find('ul', class_="nav-list")

# Get the "a" 
a_link = get_ul.find_all('a')
# print(a_link)

# declare an empty list for the a
a_list = []
# declare an empty list for the links
a_href_list = []

# loop through the "a" to get every texts and links of the categories and put in the list
for a in a_link:
    a_list.append(a.text.strip())
    a_href = a['href']
    a_href_list.append(a_href)

print(a_href_list)

# declare an empty list to keep url link of each category
url_links = []

for i in a_href_list:
    url_links.append(page_url + i)


url_links_len = len(url_links)

# for index in range(1, url_links_len):
    # url_category = url_links[index]
url_category = url_links[1]
url_page = requests.get(url_category)
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

    