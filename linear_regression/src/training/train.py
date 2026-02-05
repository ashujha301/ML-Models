from src.training.data_loader import load_feature_view
from src.training.split import train_val_test_split
from src.features.base import standardize
from src.models.core_algorithm import Linear_RegressionGD
from src.training.metrices import mse, rmse, r2_score

from sqlalchemy import text
from data.db.db_config import engine

import os
import pickle

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "linear_regression_gd.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "standardizer.pkl")

FEATURE_VIEW_BASIC_V1 = "feature_view_basic_v1"
FEATURE_VIEW_EFFICIENCY_V2 = "feature_view_efficiency_v2"
FEATURE_VIEW_HYBRID_V3 = "feature_view_hybrid_v3"
FEATURE_VIEW_INTERACTIONS_V4 = "feature_view_interactions_v4"
FEATURE_VIEW_CLICKS_V1 = "feature_view_clicks_v1"
FEATURE_VIEW_IMPRESSIONS_V1 = "feature_view_impressions_v1"
FEATURE_VIEW_HOUSING_V1 = "feature_view_housing_v1"
MODEL_NAME = "linear_regression_gd"

def log_training_run(feature_view, model_name, mse_val, rmse_val, r2_val):
    sql = """ 
        INSERT INTO training_runs 
        (feature_view, model_name, loss, rmse, r2_score)
        VALUES
        (:feature_view, :model_name, :loss, :rmse, :r2_score)

        """
    
    with engine.begin() as conn:
        conn.execute(
            text(sql),
            {
                "feature_view": feature_view,
                "model_name": model_name,
                "loss": float(mse_val),
                "rmse": float(rmse_val),
                "r2_score": float(r2_val),
            })
        

def train():
    
    # Load data
    # X, y = load_feature_view(FEATURE_VIEW_BASIC_V1)
    # X, y = load_feature_view(FEATURE_VIEW_EFFICIENCY_V2)
    # X, y = load_feature_view(FEATURE_VIEW_HYBRID_V3)
    # X, y = load_feature_view(FEATURE_VIEW_INTERACTIONS_V4)
    # X, y = load_feature_view(FEATURE_VIEW_CLICKS_V1)
    # X, y = load_feature_view(FEATURE_VIEW_IMPRESSIONS_V1)
    X, y = load_feature_view(FEATURE_VIEW_HOUSING_V1)

    # Split data
    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)

    #Scale using TRAIN stats only
    X_train, mean, std = standardize(X_train)
    X_val, _, _ = standardize(X_val, mean, std)
    X_test, _, _ = standardize(X_test, mean, std)

    # Train model
    model = Linear_RegressionGD(learning_rate=0.01, epochs=2000)
    model.fit(X_train, y_train)

    # Evaluate
    y_val_pred = model.predict(X_val)
    mse_val = mse(y_val, y_val_pred)
    rmse_val = rmse(y_val, y_val_pred)
    r2_val = r2_score(y_val, y_val_pred)

    print("Validation Metrics")
    print("MSE :", mse_val)
    print("RMSE :", rmse_val)
    print("R2 :", r2_val)

    # Log experiment
    log_training_run(
        # FEATURE_VIEW_BASIC_V1,
        # FEATURE_VIEW_EFFICIENCY_V2,
        # FEATURE_VIEW_HYBRID_V3,
        # FEATURE_VIEW_INTERACTIONS_V4,
        # FEATURE_VIEW_CLICKS_V1,
        # FEATURE_VIEW_IMPRESSIONS_V1,
        FEATURE_VIEW_HOUSING_V1,
        MODEL_NAME,
        mse_val,
        rmse_val,
        r2_val
    )

    # Save model
    os.makedirs(MODEL_DIR, exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump((mean, std), f)

    print(f"Model saved -> {MODEL_PATH }")
    print(f"Scaler saved -> {SCALER_PATH }")

if __name__ == "__main__":
    train()