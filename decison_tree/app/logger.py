import json
from sqlalchemy import text
from data.db.db_config import engine

# ----------------------------
# PREDICTION LOGGING
# ----------------------------

def log_prediction(
    model_version,
    payload,
    prediction,
    probability,
    reason,
    latency
):

    sql = """
    INSERT INTO prediction_logs
    (
        model_version,
        loan_id,
        prediction,
        probability,
        reason,
        age,
        income,
        credit_score,
        loan_amount,
        latency_ms
    )
    VALUES
    (
        :version,
        :loan_id,
        :prediction,
        :prob,
        :reason,
        :age,
        :income,
        :credit,
        :loan,
        :latency
    )
    """

    with engine.begin() as conn:
        conn.execute(text(sql), {
            "version": model_version,
            "loan_id": payload.get("loan_id"),
            "prediction": prediction,
            "prob": probability,
            "reason": reason,
            "age": payload["age"],
            "income": payload["income"],
            "credit": payload["credit_score"],
            "loan": payload["loan_amount"],
            "latency": latency
        })
