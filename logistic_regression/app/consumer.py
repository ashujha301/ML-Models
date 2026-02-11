import json
import time
import asyncio
import numpy as np
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from app.model_loader import load_model
from app.websocket_manager import manager
from app.inference_logger import add_to_batch, flush_batch, BATCH

# ---------------- CONFIG ----------------
MODEL_NAME = "logistic_regression_gd"
MODEL_VERSION = "v1"
FEATURE_VIEW = "feature_view_fraud_v1"

BUFFER_SIZE = 50          # batch size
FLUSH_INTERVAL = 5        # seconds

model, mean, std = load_model()

def start_consumer():

    # wait until kafka ready
    while True:
        try:
            consumer = KafkaConsumer(
                "transactions",
                bootstrap_servers="kafka:9092",
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest",
                group_id="fraud-group"
            )
            print("Kafka connected")
            break

        except NoBrokersAvailable:
            print("Waiting for Kafka...")
            time.sleep(5)

    print("Consumer started")

    last_flush_time = time.time()

    for msg in consumer:

        start_time = time.time()
        data = msg.value

        # ---------- feature vector ----------
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

        latency = (time.time() - start_time) * 1000
        confidence = 1 - abs(prob - 0.5)

        # ---------- realtime alert ----------
        if pred == 1:
            alert = {
                "fraud": True,
                "probability": float(prob),
                "data": data
            }

            print("FRAUD ALERT:", alert)
            asyncio.run(manager.broadcast(json.dumps(alert)))

        # ---------- logging decision ----------
        should_log = (
            pred == 1
            or (0.4 < prob < 0.6)
        )

        if should_log:
            record = {
                "model_name": MODEL_NAME,
                "model_version": MODEL_VERSION,
                "feature_view": FEATURE_VIEW,

                "transaction_id": data.get("trans_num", None),

                "prediction": pred,
                "probability": float(prob),
                "confidence": float(confidence),

                "drift_detected": False,

                "amount": data["amt"],
                "hour": data["hour"],
                "category_code": data["category_code"],

                "latency_ms": float(latency),

                "raw_payload": json.dumps(data)
            }

            add_to_batch(record)

        # ---------- flush conditions ----------
        if len(BATCH) >= BUFFER_SIZE:
            flush_batch()
            last_flush_time = time.time()

        if time.time() - last_flush_time > FLUSH_INTERVAL:
            flush_batch()
            last_flush_time = time.time()