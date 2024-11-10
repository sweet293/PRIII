from flask import Flask, request, Blueprint, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from collections import defaultdict
import websockets
import asyncio
import json
import threading

import os

# Init app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgrespassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Init db and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Product Model/Class
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10))
    link = db.Column(db.Text)
    file_path = db.Column(db.String(255))

    def __init__(self, product_name, category, price, currency, link, file_path):
        self.product_name = product_name
        self.category = category
        self.price = price
        self.currency = currency
        self.link = link
        self.file_path = file_path


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'product_name', 'category', 'price', 'currency', 'link', 'file_path')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        with open(file_path, 'r') as f:
            data = json.load(f)

        # Iterate over the product data and create new products
        for product_data in data:
            product_name = product_data['product_name']
            category = product_data['category']
            price = product_data['price']
            currency = product_data['currency']
            link = product_data['link']

            new_product = Product(product_name, category, price, currency, link, file_path)
            db.session.add(new_product)

        db.session.commit()

        return jsonify({'message': 'Products created successfully'}), 201

# Create a Product
@app.route('/products', methods=['POST'])
def add_product():
    try:
        product_name = request.json['product_name']
        category = request.json['category']
        price = request.json['price']
        currency = request.json['currency']
        link = request.json['link']

        new_product = Product(product_name, category, price, currency, link)

        db.session.add(new_product)
        db.session.commit()

        return product_schema.jsonify(new_product)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Get All Products (with Pagination)
@app.route('/products', methods=['GET'])
def get_products():
    # Handle query parameters
    category = request.args.get('category')
    name = request.args.get('name')
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    #Starts a query to fetch Product records from the database.
    query = Product.query

    if category:
        query = query.filter_by(category=category)
    elif name:
        query = query.filter(Product.product_name.ilike(f'%{name}%'))

    total_count = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'data': products_schema.dump(products),
        'meta': {
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_count + per_page - 1) // per_page
        }
    })


# Get Single Product
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return product_schema.jsonify(product)


# Update a Product
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    if 'product_name' in request.json:
        product.product_name = request.json['product_name']
    if 'category' in request.json:
        product.category = request.json['category']
    if 'price' in request.json:
        product.price = request.json['price']
    if 'currency' in request.json:
        product.currency = request.json['currency']
    if 'link' in request.json:
        product.link = request.json['link']

    db.session.commit()

    return product_schema.jsonify(product)


# Delete Product
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"})

#-----------------

connected_users = {}

@app.route('/')
def serve_client():
    return send_from_directory('.', 'index.html')  # Serve the HTML file


async def chat_handler(websocket, path):
    username = None
    try:
        while True:
            message = await websocket.recv()
            if message.startswith("join_room:"):
                username = message[len("join_room:"):].strip()
                connected_users[username] = websocket
                print(f"{username} has joined the chat.")
                for user, conn in connected_users.items():
                    if user != username:
                        await conn.send(f"{username} has joined the chat.")
                await websocket.send(f"Welcome {username}!")
                break

        async for message in websocket:
            if message == "leave_room":
                connected_users.pop(username, None)
                for user, conn in connected_users.items():
                    await conn.send(f"{username} has left the chat.")
                break
            elif message.startswith("send_msg:"):
                chat_message = message[len("send_msg:"):].strip()
                for user, conn in connected_users.items():
                    if user != username:
                        await conn.send(f"{username}: {chat_message}")
                await websocket.send(f"{username}: {chat_message}")

    except websockets.ConnectionClosed:
        if username:
            connected_users.pop(username, None)
            print(f"{username} has disconnected.")





# Function to start the WebSocket server on port 8765
async def start_websocket_server():
    server = await websockets.serve(chat_handler, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

# Function to start the Flask HTTP server on port 5000
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)

# Main function to run both servers
async def main():
    # Create database tables
    with app.app_context():
        db.create_all()

    await asyncio.gather(
        start_websocket_server(),
        asyncio.to_thread(run_flask)  # Running Flask app in a separate thread
    )


if __name__ == "__main__":
    asyncio.run(main())