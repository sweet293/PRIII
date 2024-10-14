import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://www.smart.md/smartphone"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)