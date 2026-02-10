import json
import time
import pandas as pd
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_csv("data/raw/fraudTest.csv")

for _, row in df.iterrows():

    payload = {
        "amt": float(row["amt"]),
        "lat": float(row["lat"]),
        "long": float(row["long"]),
        "hour": pd.to_datetime(row["trans_date_trans_time"]).hour,
        "category_code": hash(row["category"]) % 20
    }

    producer.send("transactions", payload)
    print("Sent:", payload)

    time.sleep(0.2)
