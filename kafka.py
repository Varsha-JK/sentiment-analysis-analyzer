import os
import time
from confluent_kafka import Consumer, Producer
import json
################
def produce(topic):
    p = Producer({'bootstrap.servers': os.getenv("bootstrap_servers")})
    print('Kafka Producer has been initiated...')

    #####################
    def receipt(err, msg):
        if err is not None:
            print('Error: {}'.format(err))
        else:
            message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
            print(message)
    data = {
        'topic': topic
    }
    m = json.dumps(data)
    analyzer_topic = os.getenv("analyzer_topic")
    p.poll(1)
    p.produce(analyzer_topic, m.encode('utf-8'), callback=receipt)
    p.flush()
