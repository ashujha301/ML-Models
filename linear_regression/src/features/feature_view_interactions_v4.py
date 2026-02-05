from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_interactions_v4"

FEATURE_VIEW_DESCRIPTION = """
Interaction-based feature view enabling linear regression
to model conditional effects between performance, cost,
and channel context.
"""

RAW_TABLE = "marketing_campaign_raw"
TARGET_COLUMN = "ROI"


def create_feature_view():
    # 1. Register feature view
    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description=FEATURE_VIEW_DESCRIPTION.strip(),
    )

    # 2. Register features (metadata)
    features = [
        "ctr",
        "cost_per_click",
        "conversion_rate",
        "ctr_x_cost_per_click",
        "conversion_x_cost_per_click",
        "google_ads_ctr",
        "instagram_ctr",
        "youtube_ctr",
    ]

    for name in features:
        registry_feature(
            feature_name=name,
            feature_view=FEATURE_VIEW_NAME,
            description=f"Interaction feature: {name}",
            data_type="numeric",
            source_column="derived",
            transformation="interaction",
        )

    # 3. Build SQL
    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        -- Base numeric
        CASE WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions" ELSE 0 END AS ctr,

        CASE WHEN "Clicks" > 0 THEN
            NULLIF(regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'), '')::float / "Clicks"
        ELSE 0 END AS cost_per_click,

        "Conversion_Rate" AS conversion_rate,

        -- Numeric interactions
        (CASE WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions" ELSE 0 END)
        *
        (CASE WHEN "Clicks" > 0 THEN
            NULLIF(regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'), '')::float / "Clicks"
        ELSE 0 END)
        AS ctr_x_cost_per_click,

        "Conversion_Rate"
        *
        (CASE WHEN "Clicks" > 0 THEN
            NULLIF(regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'), '')::float / "Clicks"
        ELSE 0 END)
        AS conversion_x_cost_per_click,

        -- Channel-conditioned CTR
        CASE WHEN "Channel_Used" = 'Google Ads'
            THEN (CASE WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions" ELSE 0 END)
            ELSE 0 END AS google_ads_ctr,

        CASE WHEN "Channel_Used" = 'Instagram'
            THEN (CASE WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions" ELSE 0 END)
            ELSE 0 END AS instagram_ctr,

        CASE WHEN "Channel_Used" = 'YouTube'
            THEN (CASE WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions" ELSE 0 END)
            ELSE 0 END AS youtube_ctr,

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
