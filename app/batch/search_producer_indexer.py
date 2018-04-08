from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(15)

consumer3 = KafkaConsumer('new-producer-topic',group_id='producer-indexer',bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])

for message in consumer3:
    #print(json.loads((message.value).decode('utf-8')))
    new_producer = json.loads((message.value).decode('utf-8'))
    es.index(index='producer_index', doc_type='producer', id=new_producer['pk'], body=new_producer)
    es.indices.refresh(index="producer_index")
