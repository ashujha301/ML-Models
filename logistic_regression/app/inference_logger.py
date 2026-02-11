import uuid
from sqlalchemy import text
from data.db.db_config import engine

BATCH = []
BATCH_ID = str(uuid.uuid4())

def add_to_batch(record):
    record["batch_id"] = BATCH_ID
    BATCH.append(record)

def flush_batch():
    global BATCH, BATCH_ID

    if not BATCH:
        return

    sql = """
    INSERT INTO inference_logs
    (
        batch_id,
        model_name,
        model_version,
        feature_view,
        transaction_id,
        prediction,
        probability,
        confidence,
        drift_detected,
        amount,
        hour,
        category_code,
        latency_ms,
        raw_payload
    )
    VALUES
    (
        :batch_id,
        :model_name,
        :model_version,
        :feature_view,
        :transaction_id,
        :prediction,
        :probability,
        :confidence,
        :drift_detected,
        :amount,
        :hour,
        :category_code,
        :latency_ms,
        :raw_payload
    )
    """

    with engine.begin() as conn:
        conn.execute(text(sql), BATCH)

    print(f"Batch inserted {len(BATCH)} rows")

    BATCH = []
    BATCH_ID = str(uuid.uuid4())
