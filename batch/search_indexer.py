from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(15)

consumer = KafkaConsumer('kafka_topic', group_id='indexer', bootstrap_servers=['kafka:9092'])

es = Elasticsearch(['es'])

# Waiting for something from Kafka
for message in consumer:
    #print(json.loads((message.value).decode('utf-8')))
    new_item = json.loads((message.value).decode('utf-8'))
    type = new_item['type']
    if type=="listing":
        es.index(index='listing_index', doc_type='listing', id=new_item['pk'], body=new_item)
        es.indices.refresh(index="listing_index")
    elif type=="consumer":
        es.index(index='consumer_index', doc_type='consumer', id=new_item['pk'], body=new_item)
        es.indices.refresh(index="consumer_index")
    elif type=="producer":
        es.index(index='producer_index', doc_type='producer', id=new_item['pk'], body=new_item)
        es.indices.refresh(index="producer_index")


