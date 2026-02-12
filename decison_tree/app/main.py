from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import time
from app import model_loader
from app.model_loader import load_active_model, watch_for_new_model, model, version
from app.logger import log_prediction
from app.drift import check_drift
from app.feature_name import FEATURE_NAMES


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting API...")

    load_active_model()

    t = threading.Thread(target=watch_for_new_model, daemon=True)
    t.start()

    yield

    print("Shutting down API")


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
def predict(payload: dict):

    start = time.time()

    x = [
        payload["age"],
        payload["income"],
        payload["loan_amount"],
        payload["credit_score"],
        payload["months_employed"],
        payload["num_credit_lines"],
        payload["interest_rate"],
        payload["loan_term"],
        payload["dti_ratio"],
        payload["education_code"],
        payload["employment_code"],
        payload["has_mortgage"],
        payload["has_dependents"],
        payload["has_cosigner"]
    ]

    pred, path = model_loader.model.predict_with_path([x])
    pred = pred[0]
    path = path[0]

    readable = []
    for step in path:
        idx = int(step.split("_")[1].split(" ")[0])
        readable.append(step.replace(f"feature_{idx}", FEATURE_NAMES[idx]))

    latency = (time.time() - start) * 1000
    drift = check_drift(payload)

    log_prediction(
        model_loader.version,
        payload,
        int(pred),
        0.0,
        " → ".join(readable),
        latency
    )

    return {
        "prediction": int(pred),
        "model_version": model_loader.version,
        "latency_ms": latency,
        "reason_path": readable,
        "drift_detected": drift
    }
