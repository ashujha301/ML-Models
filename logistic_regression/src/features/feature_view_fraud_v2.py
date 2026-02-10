from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_fraud_v2"
RAW_TABLE = "fraud_test_raw"
TARGET_COLUMN = "is_fraud"

def create_feature_view():

    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description="Fraud v2 behavioral features",
    )

    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        -- log amount
        LN(amt + 1) AS log_amt,

        -- large transaction flag
        CASE WHEN amt > 200 THEN 1 ELSE 0 END AS high_amt,

        -- hour
        EXTRACT(HOUR FROM trans_date_trans_time::timestamp) AS hour,

        -- night transaction
        CASE 
            WHEN EXTRACT(HOUR FROM trans_date_trans_time::timestamp) BETWEEN 0 AND 5
            THEN 1 ELSE 0 
        END AS night_txn,

        -- category encoding
        DENSE_RANK() OVER (ORDER BY category) AS category_code,

        -- distance between user & merchant
        SQRT(
            POWER(lat - merch_lat, 2) +
            POWER(long - merch_long, 2)
        ) AS distance,

        {TARGET_COLUMN} AS target

    FROM {RAW_TABLE}
    WHERE {TARGET_COLUMN} IS NOT NULL;
    """

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {FEATURE_VIEW_NAME};"))
        conn.execute(text(sql))

    print(f"{FEATURE_VIEW_NAME} created successfully")


if __name__ == "__main__":
    create_feature_view()
