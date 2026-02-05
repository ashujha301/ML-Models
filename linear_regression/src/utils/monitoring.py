from sqlalchemy import text
from data.db.db_config import engine

def log_prediction(model_name, feature_view, prediction, confidence, drift):
    sql = """
        INSERT INTO inference_logs
        (model_name, feature_view, prediction, confidence, drift_detected)
        VALUES
        (:model_name, :feature_view, :prediction, :confidence, :drift)
    """

    with engine.begin() as conn:
        conn.execute(text(sql), {
            "model_name": model_name,
            "feature_view": feature_view,
            "prediction": float(prediction),
            "confidence": float(confidence),
            "drift": drift
        })
