from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import (
    register_feature_view,
    registry_feature,
)

FEATURE_VIEW_NAME = "feature_view_basic_v1"

FEATURE_VIEW_DESCRIPTION = """
Baseline feature view for ROI prediction using
basic numeric engagement and performance signals.
"""

RAW_TABLE = "marketing_campaign_raw"
TARGET_COLUMN = "ROI"

FEATURES = {
    "clicks": {
        "source_column": "Clicks",
        "description": "Total number of clicks",
        "data_type": "numeric",
        "transformation": "identity",
    },
    "impressions": {
        "source_column": "Impressions",
        "description": "Total number of impressions",
        "data_type": "numeric",
        "transformation": "identity",
    },
    "engagement_score": {
        "source_column": "Engagement_Score",
        "description": "Engagement quality score",
        "data_type": "numeric",
        "transformation": "identity",
    },
    "conversion_rate": {
        "source_column": "Conversion_Rate",
        "description": "Click to conversion efficiency",
        "data_type": "numeric",
        "transformation": "identity",
    },
}


def create_feature_view():
    # 1. Register feature view
    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description=FEATURE_VIEW_DESCRIPTION.strip(),
    )

    # 2. Register features
    for feature_name, meta in FEATURES.items():
        registry_feature(
            feature_name=feature_name,
            feature_view=FEATURE_VIEW_NAME,
            description=meta["description"],
            data_type=meta["data_type"],
            source_column=meta["source_column"],
            transformation=meta["transformation"],
        )

    # 3. Materialize feature table
    feature_sql = ", ".join(
        [f'"{meta["source_column"]}" AS {name}'
         for name, meta in FEATURES.items()]
    )

    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        {feature_sql},
        "{TARGET_COLUMN}" AS target
    FROM {RAW_TABLE}
    WHERE "{TARGET_COLUMN}" IS NOT NULL;
    """

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {FEATURE_VIEW_NAME};"))
        conn.execute(text(sql))

    print(f"{FEATURE_VIEW_NAME} created successfully")


if __name__ == "__main__":
    create_feature_view()
