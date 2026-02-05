REQUIRED_FIELDS = [
    "Impressions",
    "Engagement_Score",
    "Duration",
    "Channel_Used",
    "Campaign_Type",
]

REQUIRED_FIELDS_HOUSING = [
    "median_income",
    "housing_median_age",
    "total_rooms",
    "population",
    "households",
    "latitude",
    "longitude",
]

def validate_payload(payload: dict):
    missing = set(REQUIRED_FIELDS) - set(payload.keys())
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

def validate_payload_housing(payload: dict):
    """
    Validate incoming housing payload for inference.
    Ensures all required fields exist and are numeric.
    """

    missing = set(REQUIRED_FIELDS_HOUSING) - set(payload.keys())
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    # type checks
    for field in REQUIRED_FIELDS_HOUSING:
        value = payload[field]

        if value is None:
            raise ValueError(f"{field} cannot be None")

        try:
            float(value)
        except Exception:
            raise ValueError(f"{field} must be numeric")