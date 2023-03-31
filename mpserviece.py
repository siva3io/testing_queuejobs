import consumerclass as Sc
import producerclass as pc
import sys
name = sys.argv[1]
consumer = Sc.Consumer('mainStream',name)
consumer.createExchange('direct')
consumer.createQueue()
def callback(ch,method,properties,body):
    print('in mpserviece',body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    consumer.startSending("verifiying token",'dataTransformer')
    print('completed')
consumer.startConsuming(callback)
consumer.destroy()
