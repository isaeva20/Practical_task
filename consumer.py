import pika
import os

def callback(ch, method, properties, body):
    message = body.decode()
    filename = f'output_{os.getpid()}.txt'
    with open(filename, 'a') as f:
        f.write(message + '\n')
    print(f"Получено сообщение: {message}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print('Ожидание сообщений...')
channel.start_consuming() 

