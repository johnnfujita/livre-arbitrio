import json
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":

    consumer = KafkaConsumer(
        os.getenv("KAFKA_TOPIC"),
        bootstrap_servers=os.getenv("KAFKA_BROKER_URL"),
        auto_offset_reset="earliest"
    )
    for message in consumer:
        print(json.loads(message.value))