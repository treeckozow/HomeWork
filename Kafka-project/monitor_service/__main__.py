import os
import uvicorn
from fastapi import FastAPI
from threading import Thread
from sensor_reading_controller import router
from consumer import monitorSensor

def main():
    app = FastAPI(title="IoT Monitoring API")

    app.state.SENSOR_DATA = {
        "current": {},
        "sum": {},
        "count": {}
    }

    # List of topics to consume (set via environment variable, e.g., "ac_power,washing_power" for PowerMonitor)
    kafka_topics = os.getenv("KAFKA_TOPICS", "").split(",")

    # Start a separate thread for each Kafka topic
    threads = []
    for topic in kafka_topics:
        thread = Thread(target=monitorSensor, args=(app.state.SENSOR_DATA, topic))
        thread.start()
        threads.append(thread)

    app.include_router(router)

    uvicorn.run(app, host="0.0.0.0", port=5000)

    # Wait for all consumer threads to finish
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
