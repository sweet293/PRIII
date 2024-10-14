import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://makeup.md/categorys/324237/"

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)




#------------nr3

# Base URL to prepend to relative links
base_url = "https://makeup.md"

# Find all containers that have both titles and prices
product_containers = soup.find_all("div", {"class": "simple-slider-list__link"})

# Loop through each product container and extract title and prices
for container in product_containers:
    # Extract product name
    title_tag = container.find("a", {"class": "simple-slider-list__name"})
    product_name = title_tag.get_text().strip() if title_tag else "No title"

    # Extract product link
    product_link = base_url + title_tag['href'] if title_tag else "No link"

    # Extract current price
    price_tag = container.find("span", {"class": "price_item"})
    current_price = price_tag.get_text().strip() if price_tag else "No price"

    # Extract currency
    currency_tag = container.find("span", {"class": "currency"})
    currency = currency_tag.get_text().strip() if currency_tag else "No currency"

    # Print the title and price together
    print(f"Product Name: {product_name}, Price: {current_price} {currency}, Link: {product_link}")


#------------nr4







