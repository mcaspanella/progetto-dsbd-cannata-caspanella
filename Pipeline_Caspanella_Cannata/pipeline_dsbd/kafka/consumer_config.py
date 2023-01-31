from kafka import KafkaConsumer, TopicPartition
#from kafka.structs import TopicPartition

def consumer(topicName, partition):
    bootstrap_servers = ['kafka:9092']
    consumer = KafkaConsumer (group_id = 'group1',bootstrap_servers = bootstrap_servers)
    consumer.assign([TopicPartition(topicName, partition)])
    return consumer
 

