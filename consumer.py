import consumerclass as Sc
import sys
name = sys.argv[1]
consumer = Sc.Consumer('mainStream',name)
consumer.createExchange()
consumer.createQueue()
def callback(ch,method,properties,body):
    print('%r' % (body))
consumer.startConsuming(callback)
consumer.destroy()
