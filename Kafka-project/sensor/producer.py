import os
import csv
import time
from kafka import KafkaProducer
import threading
import logging

logging.basicConfig(level=logging.INFO)

# Kafka configuration
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
producer = KafkaProducer(bootstrap_servers=f'kafka:{KAFKA_PORT}')

# Environment variables for sensor type and CSV files
SENSOR_TYPE = os.getenv("SENSOR_TYPE")
TEMP_CSV_FILE = os.getenv("TEMP_CSV_FILE")
POWER_CSV_FILE = os.getenv("POWER_CSV_FILE")
HUMIDITY_CSV_FILE = os.getenv("HUMIDITY_CSV_FILE")


# Define topics based on sensor type
TEMP_TOPIC = SENSOR_TYPE + "_temp"
POWER_TOPIC = SENSOR_TYPE + "_power"
HUMIDITY_TOPIC = SENSOR_TYPE + "_humidity"

def readAndSendData(kafka_topic, csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row['value']
            producer.send(kafka_topic, value=value.encode('utf-8'))
            logging.info("Sent data to " + kafka_topic + ": " + value)
            time.sleep(10)

# Start a thread for each CSV file and topic
threads = [
    threading.Thread(target=readAndSendData, args=(TEMP_TOPIC, TEMP_CSV_FILE)),
    threading.Thread(target=readAndSendData, args=(POWER_TOPIC, POWER_CSV_FILE)),
    threading.Thread(target=readAndSendData, args=(HUMIDITY_TOPIC, HUMIDITY_CSV_FILE))
]

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
