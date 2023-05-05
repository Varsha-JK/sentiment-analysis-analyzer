"""
Helper methods for creating the kafka-python KafkaProducer and KafkaConsumer objects.
"""

import os
import json
import ssl
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from base64 import standard_b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from kafka import KafkaProducer, KafkaConsumer
from time import sleep


def get_kafka_ssl_context():
    with NamedTemporaryFile(suffix='.crt') as cert_file, \
         NamedTemporaryFile(suffix='.key') as key_file, \
         NamedTemporaryFile(suffix='.crt') as trust_file:
        cert_file.write(os.environ['KAFKA_CLIENT_CERT'].encode('utf-8'))
        cert_file.flush()

        password = standard_b64encode(os.urandom(33))
        private_key = serialization.load_pem_private_key(
            os.environ['KAFKA_CLIENT_CERT_KEY'].encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password)
        )
        key_file.write(pem)
        key_file.flush()
        trust_file.write(os.environ['KAFKA_TRUSTED_CERT'].encode('utf-8'))
        trust_file.flush()
        ssl_context = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, cafile=trust_file.name)
        ssl_context.load_cert_chain(cert_file.name, keyfile=key_file.name, password=password)
        ssl_context.check_hostname = False

    return ssl_context


def get_kafka_brokers():
    if not os.getenv('KAFKA_URL'):
        raise RuntimeError('The KAFKA_URL config variable is not set.')

    return ['{}:{}'.format(parsedUrl.hostname, parsedUrl.port) for parsedUrl in
            [urlparse(url) for url in os.environ.get('KAFKA_URL').split(',')]]


def get_kafka_producer(acks='all', value_serializer=lambda v: json.dumps(v).encode('utf-8')):
    producer = KafkaProducer(
        bootstrap_servers=get_kafka_brokers(),
        security_protocol='SSL',
        ssl_context=get_kafka_ssl_context(),
        value_serializer=value_serializer,
        acks=acks
    )
    return producer


def producer(topic):
    kafka_topic = os.getenv("analyzer_topic")
    p = get_kafka_producer()
    print('Kafka Producer has been initiated...')
    data = {
            'topic': topic
        }
    msg = json.dumps(data)
    print(msg)
    p.send(kafka_topic, msg)
    print('Produced message on topic {} with value of {}\n'.format(kafka_topic, data))
    p.close()