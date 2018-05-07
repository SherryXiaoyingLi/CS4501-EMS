from kafka import KafkaConsumer
import json
import time
import logging

time.sleep(15)

#Reads from the log added by the request_detail service of the experience layer
consumer = KafkaConsumer('spark_topic', group_id='indexer', bootstrap_servers=['kafka:9092'])

for message in consumer:


    #retreives the access of producer_id and consumer_id from kafka
    new_access = json.loads((message.value).decode('utf-8'))
    type = new_access['type']
    user_id = new_access['user_id']
    item_id = new_access['item_id']
    #To Do: Write to the access.log file with "producer_id [new tab] consumer_request_id"
    if type == 'access':
        with open('access.txt', 'a') as the_file:
            the_file.write(str(user_id) + '\t' + str(item_id) + '\n')
