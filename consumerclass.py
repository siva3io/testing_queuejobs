import pika
import os

class Consumer:
    def __init__(self,exchangeName,queueName):
        self.queueName = queueName
        self.exchangeName = exchangeName
        self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(self.params) 
        self.channel = self.connection.channel()
    def createExchange(self,exchangeType='fanout'):
        self.channel.exchange_declare(exchange=self.exchangeName,
        exchange_type=exchangeType)
    def createQueue(self):
        self.channel.queue_declare(self.queueName)
    # def callback(self,ch,method,properties,body):
    #     print(body)
    def startConsuming(self,ff):
        self.channel.queue_bind(exchange=self.exchangeName,
        queue=self.queueName)
        self.channel.basic_consume(queue=self.queueName,
        on_message_callback =  ff)
        self.channel.start_consuming()
    def startSending(self,message,qName=''):
        self.channel.basic_publish(exchange=self.exchangeName,
        routing_key=qName,
        body=message)
    def destroy(self):
        self.channel.close()
