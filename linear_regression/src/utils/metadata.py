import datetime

def model_metadata():
    return {
        "model_name": "linear_regression_gd",
        "feature_view": "feature_view_clicks_v1",
        "timestamp": datetime.utcnow().isoformat(),
    }
