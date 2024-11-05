import json


# 1. Load data from products.json
def load_product_data(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)


# 2. Serialize data to JSON (already in JSON, so directly save it)
def write_to_json(data, output_file):
    json_str = "{\n"
    for i, product in enumerate(data):
        json_str += f'  "product_{i + 1}": {{\n'
        for key, value in product.items():
            if isinstance(value, str):
                json_str += f'    "{key}": "{value}",\n'
            else:
                json_str += f'    "{key}": {value},\n'
        json_str = json_str.rstrip(",\n") + "\n  },\n"
    json_str = json_str.rstrip(",\n") + "\n}"

    # Write to the output JSON file
    with open(output_file, 'w') as f:
        f.write(json_str)


# 3. Serialize data to XML format
def serialize_to_xml(data):
    xml_str = "<products>\n"
    for i, product in enumerate(data):
        xml_str += f'  <product_{i + 1}>\n'
        for key, value in product.items():
            xml_str += f'    <{key}>{value}</{key}>\n'
        xml_str += f'  </product_{i + 1}>\n'
    xml_str += "</products>"
    return xml_str


# 4. Write XML data to a file
def write_to_xml(data, output_file):
    xml_output = serialize_to_xml(data)
    with open(output_file, 'w') as f:
        f.write(xml_output)


# 5. Main function to handle everything
def process_product_data(input_json, output_json_file, output_xml_file):
    # Load product data from the input JSON file
    products = load_product_data(input_json)

    # Write to JSON file
    write_to_json(products, output_json_file)

    # Write to XML file
    write_to_xml(products, output_xml_file)


# Example usage
input_json_file = 'products.json'  # Source JSON file
output_json_file = 'output_products.json'  # Destination JSON file
output_xml_file = 'output_products.xml'  # Destination XML file

# Process the product data and write to JSON and XML
process_product_data(input_json_file, output_json_file, output_xml_file)
