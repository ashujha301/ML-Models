from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_impressions_v1"
RAW_TABLE = "marketing_campaign_raw"
TARGET_COLUMN = "Impressions"

FEATURE_VIEW_DESCRIPTION = """
Feature view for predicting campaign impressions.
Impressions are upstream, additive, and budget/duration driven.
Well-suited for linear regression.
"""

FEATURES = {
    "duration_days": {
        "description": "Campaign duration in days",
        "data_type": "numeric",
        "source_column": "Duration",
        "transformation": "text_to_int_days",
    },
    "acquisition_cost": {
        "description": "Campaign acquisition cost",
        "data_type": "numeric",
        "source_column": "Acquisition_Cost",
        "transformation": "currency_text_to_float",
    },
    "channel_google_ads": {
        "description": "Google Ads channel",
        "data_type": "binary",
        "source_column": "Channel_Used",
        "transformation": "one_hot",
    },
    "channel_instagram": {
        "description": "Instagram channel",
        "data_type": "binary",
        "source_column": "Channel_Used",
        "transformation": "one_hot",
    },
    "channel_youtube": {
        "description": "YouTube channel",
        "data_type": "binary",
        "source_column": "Channel_Used",
        "transformation": "one_hot",
    },
    "campaign_email": {
        "description": "Email campaign type",
        "data_type": "binary",
        "source_column": "Campaign_Type",
        "transformation": "one_hot",
    },
    "campaign_display": {
        "description": "Display campaign type",
        "data_type": "binary",
        "source_column": "Campaign_Type",
        "transformation": "one_hot",
    },
    "campaign_influencer": {
        "description": "Influencer campaign type",
        "data_type": "binary",
        "source_column": "Campaign_Type",
        "transformation": "one_hot",
    },
}

def create_feature_view():
    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description=FEATURE_VIEW_DESCRIPTION.strip(),
    )

    for name, meta in FEATURES.items():
        registry_feature(
            feature_name=name,
            feature_view=FEATURE_VIEW_NAME,
            description=meta["description"],
            data_type=meta["data_type"],
            source_column=meta["source_column"],
            transformation=meta["transformation"],
        )

    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        regexp_replace("Duration", '[^0-9]', '', 'g')::int AS duration_days,

        NULLIF(
            regexp_replace("Acquisition_Cost", '[^0-9.]', '', 'g'),
            ''
        )::float AS acquisition_cost,

        CASE WHEN "Channel_Used" = 'Google Ads' THEN 1 ELSE 0 END AS channel_google_ads,
        CASE WHEN "Channel_Used" = 'Instagram' THEN 1 ELSE 0 END AS channel_instagram,
        CASE WHEN "Channel_Used" = 'YouTube' THEN 1 ELSE 0 END AS channel_youtube,

        CASE WHEN "Campaign_Type" = 'Email' THEN 1 ELSE 0 END AS campaign_email,
        CASE WHEN "Campaign_Type" = 'Display' THEN 1 ELSE 0 END AS campaign_display,
        CASE WHEN "Campaign_Type" = 'Influencer' THEN 1 ELSE 0 END AS campaign_influencer,

        "{TARGET_COLUMN}"::float AS target
    FROM {RAW_TABLE}
    WHERE "{TARGET_COLUMN}" IS NOT NULL;
    """

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {FEATURE_VIEW_NAME};"))
        conn.execute(text(sql))

    print(f"{FEATURE_VIEW_NAME} created successfully")

if __name__ == "__main__":
    create_feature_view()
