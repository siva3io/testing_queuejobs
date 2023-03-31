import producerclass as pc
import sys
message = sys.argv[1]
producer = pc.Producer('direct','mainStream')
producer.createExchange()
producer.startSending(message,'mpserviece')
print("message Sent Successfully")
producer.destroy()
