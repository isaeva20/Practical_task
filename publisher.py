import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

with open('input.txt', 'r') as f:
    for line in f:
        message = line.strip()
        channel.basic_publish(exchange='logs', routing_key='', body=message)
        print(f"Отправлено сообщение: {message}")
        time.sleep(1)

connection.close()
