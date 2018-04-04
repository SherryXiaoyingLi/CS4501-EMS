from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(5)
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

# Waiting for something from Kafka
for message in consumer:
    #print(json.loads((message.value).decode('utf-8')))
    new_listing = json.loads((message.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
    es.indices.refresh(index="listing_index")
