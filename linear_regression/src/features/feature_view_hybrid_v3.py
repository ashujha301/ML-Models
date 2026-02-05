from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_hybrid_v3"

FEATURE_VIEW_DESCRIPTION = """
Hybrid feature view combining numeric efficiency signals
with categorical context (channel and campaign type).
"""

RAW_TABLE = "marketing_campaign_raw"
TARGET_COLUMN = "ROI"


def create_feature_view():
    # 1. Register feature view
    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description=FEATURE_VIEW_DESCRIPTION.strip(),
    )

    # 2. Register numeric features
    numeric_features = {
        "ctr": "Clicks / Impressions",
        "engagement_per_click": "Engagement_Score / Clicks",
        "cost": "Parsed Acquisition_Cost",
        "cost_per_click": "Cost / Clicks",
        "conversion_rate": "Conversion_Rate",
    }

    for name, transform in numeric_features.items():
        registry_feature(
            feature_name=name,
            feature_view=FEATURE_VIEW_NAME,
            description=f"Numeric feature: {name}",
            data_type="numeric",
            source_column="multiple",
            transformation=transform,
        )

    # 3. Register categorical features
    categorical_features = [
        "channel_google_ads",
        "channel_instagram",
        "channel_youtube",
        "channel_facebook",
        "channel_website",
        "campaign_email",
        "campaign_display",
        "campaign_influencer",
        "campaign_search",
        "campaign_social_media",
    ]

    for name in categorical_features:
        registry_feature(
            feature_name=name,
            feature_view=FEATURE_VIEW_NAME,
            description=f"One-hot encoded feature: {name}",
            data_type="binary",
            source_column="Channel_Used or Campaign_Type",
            transformation="one_hot",
        )

    # 4. Build SQL
    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        -- Numeric features
        CASE WHEN "Impressions" > 0 THEN "Clicks"::float / "Impressions" ELSE 0 END AS ctr,
        CASE WHEN "Clicks" > 0 THEN "Engagement_Score"::float / "Clicks" ELSE 0 END AS engagement_per_click,

        NULLIF(
            regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'),
            ''
        )::float AS cost,

        CASE WHEN "Clicks" > 0 THEN
            NULLIF(
                regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'),
                ''
            )::float / "Clicks"
        ELSE 0 END AS cost_per_click,

        "Conversion_Rate" AS conversion_rate,

        -- Channel one-hot
        CASE WHEN "Channel_Used" = 'Google Ads' THEN 1 ELSE 0 END AS channel_google_ads,
        CASE WHEN "Channel_Used" = 'Instagram' THEN 1 ELSE 0 END AS channel_instagram,
        CASE WHEN "Channel_Used" = 'YouTube' THEN 1 ELSE 0 END AS channel_youtube,
        CASE WHEN "Channel_Used" = 'Facebook' THEN 1 ELSE 0 END AS channel_facebook,
        CASE WHEN "Channel_Used" = 'Website' THEN 1 ELSE 0 END AS channel_website,

        -- Campaign type one-hot
        CASE WHEN "Campaign_Type" = 'Email' THEN 1 ELSE 0 END AS campaign_email,
        CASE WHEN "Campaign_Type" = 'Display' THEN 1 ELSE 0 END AS campaign_display,
        CASE WHEN "Campaign_Type" = 'Influencer' THEN 1 ELSE 0 END AS campaign_influencer,
        CASE WHEN "Campaign_Type" = 'Search' THEN 1 ELSE 0 END AS campaign_search,
        CASE WHEN "Campaign_Type" = 'Social Media' THEN 1 ELSE 0 END AS campaign_social_media,

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
