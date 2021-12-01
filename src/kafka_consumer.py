import json
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":

    consumer = KafkaConsumer(
        "high-bid-low-ask-low-latency",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest"
    )
    for message in consumer:
        print(json.loads(message.value))