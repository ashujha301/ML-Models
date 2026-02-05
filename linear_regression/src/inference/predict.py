import numpy as np

from src.inference.loader import load_model, load_scaler
from src.inference.transformer import transform_payload, transform_payload_housing
from src.utils.data_validation import validate_payload, validate_payload_housing
from src.utils.confidence import compute_confidence
from src.utils.drift import detect_drift
from src.utils.numerical_checks import validate_prediction_value
from src.utils.monitoring import log_prediction

MODEL_NAME = "linear_regression_gd"
FEATURE_VIEW = "feature_view_housing_v1"

model = load_model()
mean, std = load_scaler()

def predict(payload: dict):

    # validate_payload(payload)
    validate_payload_housing(payload)

    # Transform
    x = transform_payload_housing(payload)

    # Standardize
    x_scaled = (x - mean) / std
    x_scaled = x_scaled.reshape(1, -1)

    # Predict
    # y_log = model.predict(x_scaled)[0]
    # validate_prediction_value(y_log)
    # predicted_clicks = np.exp(y_log) - 1

    # 4. Predict (NO exp for housing)
    prediction = model.predict(x_scaled)[0]
    validate_prediction_value(prediction)

    # Confidence
    confidence = compute_confidence(x_scaled.flatten())

    # Drift
    drift = detect_drift(x_scaled.flatten())

    # Log prediction
    log_prediction(
        MODEL_NAME,
        FEATURE_VIEW,
        # predicted_clicks,
        prediction,
        confidence,
        drift
    )
    
    #For marketing clicks prediction
    # return {
    #     "predicted_clicks": float(predicted_clicks),
    #     "confidence": confidence,
    #     "drift_detected": drift,
    #     "model": MODEL_NAME
    # }

    # For housing prediction
    return {
        "predicted_price": float(prediction),
        "confidence": confidence,
        "drift_detected": drift,
        "model": MODEL_NAME,
        "feature_view": FEATURE_VIEW
    }
