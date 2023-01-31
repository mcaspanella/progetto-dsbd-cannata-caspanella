from kafka import KafkaProducer
from kafka import KafkaAdminClient
from kafka import KafkaClient
from kafka.admin import NewPartitions
import pandas as pd 
import snappy
import json
def send_msg(dataset, part):
    
    data = json.dumps(dataset.to_dict())

    compressed_data = snappy.compress(data)
    topic = 'prometheusdata'
    producer = KafkaProducer(bootstrap_servers='kafka:9092')
    partitions = producer.partitions_for(topic)
    client = KafkaAdminClient(bootstrap_servers='kafka:9092')
    
    if(len(partitions)==1):
        client.create_partitions({topic: NewPartitions(5)})
    
    producer.send(topic, compressed_data, partition=part)
    
    producer.flush()
