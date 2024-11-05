import requests
from bs4 import BeautifulSoup
import json
from functools import reduce
from datetime import datetime

# Define the conversion rates
MDL_TO_EUR = 0.052
EUR_TO_MDL = 19.29

# Define the price range for filtering
PRICE_MIN = 10  # Minimum price in MDL
PRICE_MAX = 500  # Maximum price in MDL

# Load the products from the JSON file
with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Function to convert price based on currency
def convert_price(product):
    price = product['price']
    if product['currency'] == 'MDL':
        product['price_eur'] = price * MDL_TO_EUR
    elif product['currency'] == 'EUR':
        product['price_eur'] = price * EUR_TO_MDL
    else:
        product['price_eur'] = price  # Default case
    return product

# Use map to convert all product prices
products_with_prices = list(map(convert_price, products))

# Function to filter products based on price range
def filter_by_price(product):
    return PRICE_MIN <= product['price'] <= PRICE_MAX

# Filter products within the defined price range
filtered_products = list(filter(filter_by_price, products_with_prices))

# Use reduce to sum up the prices of the filtered products
total_price_mdl = reduce(lambda acc, product: acc + product['price'], filtered_products, 0)

# Create the final data structure with timestamp and total price
final_data = {
    'timestamp': datetime.utcnow().isoformat(),
    'filtered_products': filtered_products,
    'total_price_mdl': total_price_mdl
}

# Write the final data to a JSON file
with open('filtered_products.json', 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=4)

print("Filtered products and total price have been written to filtered_products.json.")
