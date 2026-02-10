import json
import numpy as np
import asyncio
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from app.model_loader import load_model
from app.websocket_manager import manager

model, mean, std = load_model()

def start_consumer():

    # 🔁 Retry until Kafka ready
    while True:
        try:
            consumer = KafkaConsumer(
                "transactions",
                bootstrap_servers="kafka:9092",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="fraud-group"
            )
            print("✅ Kafka consumer connected")
            break

        except NoBrokersAvailable:
            print("⏳ Waiting for Kafka to be ready...")
            time.sleep(5)

    print("🚀 Kafka consumer started")

    for msg in consumer:
        data = msg.value
        print("Incoming:", data)

        x = np.array([
            data["amt"],
            data["lat"],
            data["long"],
            data["hour"],
            data["category_code"]
        ], dtype=float)

        x_scaled = (x - mean) / std
        prob = model.predict_proba(x_scaled.reshape(1, -1))[0]

        pred = int(prob >= 0.13)

        if pred == 1:
            alert = {
                "fraud": True,
                "probability": float(prob),
                "data": data
            }

            print("🚨 FRAUD ALERT:", alert)

            asyncio.run(manager.broadcast(json.dumps(alert)))