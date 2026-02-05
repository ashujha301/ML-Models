from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import (
    register_feature_view,
    registry_feature,
)

FEATURE_VIEW_NAME = "feature_view_efficiency_v2"

FEATURE_VIEW_DESCRIPTION = """
Efficiency and cost-based feature view for ROI prediction.
Adds normalized engagement and spending signals.
"""

RAW_TABLE = "marketing_campaign_raw"
TARGET_COLUMN = "ROI"

FEATURES = {
        "ctr": {
            "description": "Click-through rate (Clicks / Impressions)",
            "data_type": "numeric",
            "source_column": "Clicks, Impressions",
            "transformation": "Clicks / Impressions",
        },
        "engagement_per_click": {
            "description": "Engagement score per click",
            "data_type": "numeric",
            "source_column": "Engagement_Score, Clicks",
            "transformation": "Engagement_Score / Clicks",
        },
        "cost": {
            "description": "Parsed acquisition cost",
            "data_type": "numeric",
            "source_column": "Acquisition_Cost",
            "transformation": "currency_text_to_float",
        },
        "cost_per_click": {
            "description": "Cost per click",
            "data_type": "numeric",
            "source_column": "Acquisition_Cost, Clicks",
            "transformation": "cost / Clicks",
        },
        "conversion_rate": {
            "description": "Conversion rate",
            "data_type": "numeric",
            "source_column": "Conversion_Rate",
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
    # feature_sql = ", ".join(
    #     [f'"{meta["source_column"]}" AS {name}'
    #      for name, meta in FEATURES.items()]
    # )

    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        CASE
            WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions"
            ELSE 0
        END AS ctr,

        CASE
            WHEN "Clicks" > 0 THEN "Engagement_Score"::float / "Clicks"
            ELSE 0
        END AS engagement_per_click,

        NULLIF(
            regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'),
            ''
        )::float AS cost,

        CASE
            WHEN "Clicks" > 0 THEN
                NULLIF(
                    regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'),
                    ''
                )::float / "Clicks"
            ELSE 0
        END AS cost_per_click,

        "Conversion_Rate" AS conversion_rate,

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
