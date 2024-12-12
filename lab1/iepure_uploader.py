import pika

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
    publish_message("test")