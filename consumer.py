import json
import logging 
from kafka import KafkaConsumer

def forgiving_json_deserializer(v):
    if v is None : return
    try:
        return json.loads(v.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        logging.exception('Unable to decode: %s', v)
        return None

# topic, broker list
consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
    # (1) consume from the tail of the topic instead: 
    #  auto_offset_reset='latest'
    # (2) start a new topic: 
    # consumer.subscribe(['offering_new_too'])
     enable_auto_commit=True,
     group_id='1',
    #  value_deserializer=lambda x: loads(x.decode('utf-8')),
     value_deserializer=forgiving_json_deserializer,
     consumer_timeout_ms=1000
)

# # consume json messages
# KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))

# consumer list를 가져온다
print('[begin] get consumer list')
for message in consumer:
    print("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s" % (
        message.topic, message.partition, message.offset, message.key, message.value
    ))
print('[end] get consumer list')
