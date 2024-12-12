import pika

def consume_messages(rabbitmq_host='localhost', queue_name='queue'):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Declare the queue to ensure it exists
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        print(f"[x] Received message: {body.decode('utf-8')}")

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set up consumption of the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print("[x] Waiting for messages. To exit, press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("[x] Stopping consumer")
        connection.close()

if __name__ == "__main__":
    consume_messages()