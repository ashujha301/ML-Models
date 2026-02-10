from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_fraud_v1"

FEATURE_VIEW_DESCRIPTION = """
Baseline fraud detection feature view.
Includes transaction amount, location, time, and category.
Designed for logistic regression from scratch.
"""

RAW_TABLE = "fraud_test_raw"
TARGET_COLUMN = "is_fraud"

FEATURES = {
    "amt": {
        "source_column": "amt",
        "description": "Transaction amount",
        "data_type": "numeric",
        "transformation": "identity",
    },
    "lat": {
        "source_column": "lat",
        "description": "Transaction latitude",
        "data_type": "numeric",
        "transformation": "identity",
    },
    "long": {
        "source_column": "long",
        "description": "Transaction longitude",
        "data_type": "numeric",
        "transformation": "identity",
    },
    "hour": {
        "source_column": "trans_date_trans_time",
        "description": "Hour of transaction",
        "data_type": "numeric",
        "transformation": "extract_hour",
    },
    "category_code": {
        "source_column": "category",
        "description": "Encoded merchant category",
        "data_type": "numeric",
        "transformation": "category_encoding",
    },
}


def create_feature_view():

    # Register feature view
    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description=FEATURE_VIEW_DESCRIPTION.strip(),
    )

    # Register features
    for feature_name, meta in FEATURES.items():
        registry_feature(
            feature_name=feature_name,
            feature_view=FEATURE_VIEW_NAME,
            description=meta["description"],
            data_type=meta["data_type"],
            source_column=meta["source_column"],
            transformation=meta["transformation"],
        )

    # Materialize feature table
    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        amt,
        lat,
        long,

        EXTRACT(HOUR FROM trans_date_trans_time::timestamp) AS hour,

        DENSE_RANK() OVER (ORDER BY category) AS category_code,

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
