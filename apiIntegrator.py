from mws import Reports
from mws import Products
import mwsClient as mwsc
import json,pprint
import time
import sys
import consumerclass as Sc
def process(body):
    ReportRequestId = mwsc.request_report()
    GeneratedReportId = mwsc.getReportRequestList(ReportRequestId)
    s=mwsc.getReport('16549088718018149')
    # print(s)
    print("get report completed")
    mwsc.getProductWithASIN(s)
name = sys.argv[1]
consumer = Sc.Consumer('mainStream',name)
consumer.createExchange('direct')
consumer.createQueue()
def callback(ch,method,properties,body):
    process(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # print('completed')
consumer.startConsuming(callback)
consumer.destroy()
