import pika
import json

def publish_message(message, rabbitmq_host = 'localhost', queue_name = 'queue'):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )

    connection.close()

if __name__ == '__main__':
    # Read the contents of products.json
    try:
        with open('products.json', 'r') as file:
            products_data = json.load(file)  # Load JSON into a Python dictionary
            message = json.dumps(products_data)  # Convert to a JSON string
            print(message)
            publish_message(message)
    except FileNotFoundError:
        print("Error: 'products.json' file not found.")
    except json.JSONDecodeError:
        print("Error: 'products.json' contains invalid JSON.")