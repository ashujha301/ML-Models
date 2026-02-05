import numpy as np
import re

def transform_payload(payload: dict) -> np.ndarray:
    """
    Convert raw payload → feature vector in SAME order as training
    """

    log_impressions = np.log(float(payload["Impressions"]) + 1)
    engagement_score = float(payload["Engagement_Score"])
    duration_days = int(re.sub(r"\D", "", payload["Duration"]))

    channel = payload["Channel_Used"]
    campaign = payload["Campaign_Type"]

    features = [
        log_impressions,
        engagement_score,
        duration_days,

        1 if channel == "Google Ads" else 0,
        1 if channel == "Instagram" else 0,
        1 if channel == "YouTube" else 0,

        1 if campaign == "Email" else 0,
        1 if campaign == "Display" else 0,
        1 if campaign == "Influencer" else 0,
    ]

    return np.array(features, dtype=float)

def transform_payload_housing(payload: dict):
    return np.array([
        payload["median_income"],
        payload["housing_median_age"],
        payload["total_rooms"],
        payload["population"],
        payload["households"],
        payload["latitude"],
        payload["longitude"],
    ], dtype=float)