import os
from kafka import KafkaConsumer
import logging

logging.basicConfig(level=logging.INFO)

def monitorSensor(sensor_data, topic):
    # Kafka configuration
    KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")

    # Initialize Kafka Consumer for the specific topic
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers="kafka:" + KAFKA_PORT,
        auto_offset_reset='earliest',
        group_id=topic + "_group"
    )

    for message in consumer:
        value = float(message.value.decode('utf-8'))

        # Initialize data structure for new appliance type if not already in sensor_data
        if topic not in sensor_data["sum"]:
            sensor_data["sum"][topic] = 0
            sensor_data["count"][topic] = 0

        # Update sum and count for the appliance type based on the topic
        sensor_data["sum"][topic] += value
        sensor_data["count"][topic] += 1

        logging.info(topic + " - Received: " + str(value) + ", Total Sum: " + str(sensor_data['sum'][topic]) + ", Count: " + str(sensor_data['count'][topic]))
