import json

# Custom serialization function
def custom_serialize(data):
    serialized_data = ""
    for product in data:
        for key, value in product.items():
            serialized_data += f'{key} = "{value}"\n' if isinstance(value, str) else f'{key} = {value}\n'
        serialized_data += "\n"  # Separate products with a newline
    return serialized_data.strip()

# Custom deserialization function
def custom_deserialize(serialized_data):
    products = []
    product = {}
    for line in serialized_data.splitlines():
        if not line.strip():  # Newline between products
            if product:
                products.append(product)
                product = {}
            continue
        key, value = line.split(" = ", 1)
        value = value.strip('"') if '"' in value else int(value)
        product[key] = value
    if product:
        products.append(product)  # Add the last product
    return products

# Read data from products.json
def load_product_data(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

# Save serialized data to a file
def save_serialized_data(serialized_data, output_file):
    with open(output_file, 'w') as f:
        f.write(serialized_data)

# Load serialized data from a file
def load_serialized_data(input_file):
    with open(input_file, 'r') as f:
        return f.read()

# Example usage
def main():
    # Load the product data from products.json
    products = load_product_data('products.json')

    # Serialize the data
    serialized_data = custom_serialize(products)
    print("Serialized Data:")
    print(serialized_data)

    # Save serialized data to a file
    save_serialized_data(serialized_data, 'custom_serialized.txt')

    # Load serialized data from the file
    serialized_data_from_file = load_serialized_data('custom_serialized.txt')

    # Deserialize the data
    deserialized_data = custom_deserialize(serialized_data_from_file)
    print("\nDeserialized Data:")
    print(deserialized_data)

# Run the main function
main()

