import numpy as np
from sqlalchemy import text
from data.db.db_config import engine

BASELINE = {
    "income": 50000,
    "credit_score": 650,
    "loan_amount": 15000
}

THRESHOLD = 0.25


def check_drift(payload):

    drift_found = False

    for feature, baseline in BASELINE.items():

        value = payload[feature]
        score = abs(value - baseline) / baseline

        if score > THRESHOLD:
            drift_found = True

            sql = """
            INSERT INTO drift_events
            (feature_name, current_mean, baseline_mean, drift_score, threshold)
            VALUES
            (:f, :cur, :base, :score, :th)
            """

            with engine.begin() as conn:
                conn.execute(text(sql), {
                    "f": feature,
                    "cur": value,
                    "base": baseline,
                    "score": score,
                    "th": THRESHOLD
                })

    return drift_found
