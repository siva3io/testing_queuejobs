import pika
import os

class Producer:
    def __init__(self, exchangeType,exchangeName):
        self.exchangeType = exchangeType
        self.exchangeName = exchangeName
        self.url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        self.connection = pika.BlockingConnection(self.params) 
    def createExchange(self):
        self.channel.exchange_declare(exchange=self.exchangeName,
        exchange_type=self.exchangeType)
    def startSending(self,message,routing=''):
        self.channel.basic_publish(exchange=self.exchangeName,
        routing_key=routing,
        body=message)
    def destroy(self):
        self.channel.close()
