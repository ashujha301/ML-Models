import numpy as np
from sqlalchemy import text
from data.db.db_config import engine

BASELINE = {
    "income": 50000,
    "credit_score": 650,
    "loan_amount": 15000
}

THRESHOLD = 0.25   # feature-level threshold
ALERT_THRESHOLD = 0.4  # overall drift alert


def check_drift(payload, model_version):
    total_score = 0
    count = 0
    drift_triggered = False

    for feature, baseline in BASELINE.items():

        value = float(payload[feature])
        score = abs(value - baseline) / baseline

        total_score += score
        count += 1

        # log only if feature drift high
        if score > THRESHOLD:
            drift_triggered = True

            sql = """
            INSERT INTO drift_events
            (model_version, feature_name, drift_score, threshold)
            VALUES
            (:v, :f, :score, :th)
            """

            with engine.begin() as conn:
                conn.execute(text(sql), {
                    "v": model_version,
                    "f": feature,
                    "score": float(score),
                    "th": THRESHOLD
                })

    overall_score = total_score / count if count else 0

    return overall_score, overall_score > ALERT_THRESHOLD
