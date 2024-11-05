import time
import requests
from bs4 import BeautifulSoup
import json

# URL of the website to scrape
url = "https://makeup.md/categorys/324237/"

page = requests.get(url)
time.sleep(5)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)




#------------nr3

# Base URL to prepend to relative links
base_url = "https://makeup.md"

# Find all containers that have both titles and prices
product_containers = soup.find_all("div", {"class": "simple-slider-list__link"})

# List to store product data
products = []

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

    # Scrape the link further to extract additional data
    product_page = requests.get(product_link)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')

    # Extract product name and category from the h1 tag
    product_description_tag = product_soup.find("h1", itemprop="name")
    product_category_tag = product_soup.find("span", class_="product-item__category")

    # Extracting the product name and category
    product_category = product_category_tag.get_text().strip() if product_category_tag else "No category"

    # Print the title and price together
    #print(f"Product Name: {product_name}, Category: {product_category}, Price: {current_price} {currency}, Link: {product_link}")


#------------nr5

    # Data Validation
    #The condition checks if product_name, product_link, current_price, and current_price.isdigit() (to ensure the price is numeric) are valid. If any of these values are missing or invalid, it prints a message indicating the issue.
    if product_name and product_link and current_price and current_price.isdigit():
        # Ensure current_price is a non-negative integer
        current_price = int(current_price)  # Convert to int for storage

        if current_price >= 0:
            # Store the validated product information
            products.append({
                'product_name': product_name,
                'category': product_category,
                'price': current_price,
                'currency': currency,
                'link': product_link
            })
        else:
            print(f"Invalid price for {product_name}: {current_price}")
    else:
        print(
            f"Missing or invalid data for {product_name}. Title: '{product_name}', Link: '{product_link}', Price: '{current_price}'")

# Write the products to a JSON file, overwriting the existing file
#with open('products.json', 'w', encoding='utf-8') as f:
    #json.dump(products, f, ensure_ascii=False, indent=4)

print("Product information has been written to products.json.")



