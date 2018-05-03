from kafka import KafkaConsumer
import json
import time

time.sleep(15)

#Reads from the log added by the request_detail service of the experience layer
consumer = KafkaConsumer('new-access-topic', group_id='access-indexer', bootstrap_servers=['kafka:9092'])

for message in consumer:
    #print(json.loads((message.value).decode('utf-8')))
    
    #retreives the access of producer_id and consumer_id from kafka
    new_access = json.loads((message.value).decode('utf-8'))

    #To Do: Write to the access.log file with "producer_id [new tab] consumer_request_id"
