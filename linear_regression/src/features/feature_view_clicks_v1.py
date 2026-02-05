from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import (
    register_feature_view,
    registry_feature,
)

FEATURE_VIEW_NAME = "feature_view_clicks_v1"

FEATURE_VIEW_DESCRIPTION = """
Feature view for predicting campaign Clicks.
Designed for linear regression with additive effects:
exposure, engagement, duration, channel, and campaign type.
"""

RAW_TABLE = "marketing_campaign_raw"
TARGET_COLUMN = "Clicks"

FEATURES = {
    "impressions": {
        "description": "Number of impressions (primary exposure driver)",
        "data_type": "numeric",
        "source_column": "Impressions",
        "transformation": "identity",
    },
    "engagement_score": {
        "description": "Engagement score indicating audience interest",
        "data_type": "numeric",
        "source_column": "Engagement_Score",
        "transformation": "identity",
    },
    "duration_days": {
        "description": "Campaign duration in days",
        "data_type": "numeric",
        "source_column": "Duration",
        "transformation": "text_to_int_days",
    },

    # Channel one-hot
    "channel_google_ads": {
        "description": "Campaign run on Google Ads",
        "data_type": "binary",
        "source_column": "Channel_Used",
        "transformation": "one_hot",
    },
    "channel_instagram": {
        "description": "Campaign run on Instagram",
        "data_type": "binary",
        "source_column": "Channel_Used",
        "transformation": "one_hot",
    },
    "channel_youtube": {
        "description": "Campaign run on YouTube",
        "data_type": "binary",
        "source_column": "Channel_Used",
        "transformation": "one_hot",
    },

    # Campaign type one-hot
    "campaign_email": {
        "description": "Email-based campaign",
        "data_type": "binary",
        "source_column": "Campaign_Type",
        "transformation": "one_hot",
    },
    "campaign_display": {
        "description": "Display advertising campaign",
        "data_type": "binary",
        "source_column": "Campaign_Type",
        "transformation": "one_hot",
    },
    "campaign_influencer": {
        "description": "Influencer marketing campaign",
        "data_type": "binary",
        "source_column": "Campaign_Type",
        "transformation": "one_hot",
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
    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        LN("Impressions"::float + 1) AS log_impressions,
        "Engagement_Score"::float AS engagement_score,

        -- Duration parsing (e.g. "30 days" → 30)
        regexp_replace("Duration", '[^0-9]', '', 'g')::int AS duration_days,

        -- Channel one-hot
        CASE WHEN "Channel_Used" = 'Google Ads' THEN 1 ELSE 0 END AS channel_google_ads,
        CASE WHEN "Channel_Used" = 'Instagram' THEN 1 ELSE 0 END AS channel_instagram,
        CASE WHEN "Channel_Used" = 'YouTube' THEN 1 ELSE 0 END AS channel_youtube,

        -- Campaign type one-hot
        CASE WHEN "Campaign_Type" = 'Email' THEN 1 ELSE 0 END AS campaign_email,
        CASE WHEN "Campaign_Type" = 'Display' THEN 1 ELSE 0 END AS campaign_display,
        CASE WHEN "Campaign_Type" = 'Influencer' THEN 1 ELSE 0 END AS campaign_influencer,

        LN("{TARGET_COLUMN}"::float + 1) AS target
    FROM {RAW_TABLE}
    WHERE "{TARGET_COLUMN}" IS NOT NULL;
    """

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {FEATURE_VIEW_NAME};"))
        conn.execute(text(sql))

    print(f"{FEATURE_VIEW_NAME} created successfully")


if __name__ == "__main__":
    create_feature_view()
