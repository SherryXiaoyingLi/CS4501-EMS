from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(15)
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

# Waiting for something from Kafka
for message in consumer:
    #print(json.loads((message.value).decode('utf-8')))
    new_listing = json.loads((message.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=new_listing['pk'], body=new_listing)
    es.indices.refresh(index="listing_index")

'''
consumer2 = KafkaConsumer('new-consumer-topic',group_id='consumer-indexer',bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

for message in consumer2:
    #print(json.loads((message.value).decode('utf-8')))
    new_consumer = json.loads((message.value).decode('utf-8'))
    es.index(index='consumer_index', doc_type='consumer', id=new_consumer['pk'], body=new_consumer)
    es.indices.refresh(index="consumer_index")

consumer3 = KafkaConsumer('new-producer-topic',group_id='producer-indexer',bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

for message in consumer3:
    #print(json.loads((message.value).decode('utf-8')))
    new_producer = json.loads((message.value).decode('utf-8'))
    es.index(index='producer_index', doc_type='producer', id=new_producer['pk'], body=new_producer)
    es.indices.refresh(index="producer_index")
'''
