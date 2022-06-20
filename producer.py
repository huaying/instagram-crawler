from kafka import KafkaProducer 
import json 
import time 

producer = KafkaProducer(
    acks=0, 
    compression_type='gzip', 
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
) 

# 인스타그램 정보 불러오는 코드 작성
start = time.time() 

file_path = "./output.json"
with open(file_path, 'r') as file:
    data = json.load(file)
    producer.send('test', value=data) 
    producer.flush() 

print("elapsed :", time.time() - start)
