import consumerclass as Sc
import producerclass as pc
import sys
name = sys.argv[1]
consumer = Sc.Consumer('mainStream',name)
consumer.createExchange('direct')
consumer.createQueue()
def callback(ch,method,properties,body):
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    consumer.startSending("api integrator",'apiIntegrator')
    print('completed')
consumer.startConsuming(callback)
consumer.destroy()
