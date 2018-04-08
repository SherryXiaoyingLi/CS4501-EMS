from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(15)

consumer2 = KafkaConsumer('new-consumer-topic',group_id='consumer-indexer',bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

for message in consumer2:
    #print(json.loads((message.value).decode('utf-8')))
    new_consumer = json.loads((message.value).decode('utf-8'))
    es.index(index='consumer_index', doc_type='consumer', id=new_consumer['pk'], body=new_consumer)
    es.indices.refresh(index="consumer_index")


