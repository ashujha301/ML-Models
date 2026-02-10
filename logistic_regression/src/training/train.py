from src.training.data_loader import load_feature_view
from src.training.split import train_val_test_split
from src.features.base import standardize

from src.model.core_algorithm import LogisticRegressionGD

from src.training.metrics import (
    accuracy,
    precision,
    recall,
    f1_score,
)

from sqlalchemy import text
from data.db.db_config import engine

import os
import pickle

# PATHS
MODEL_DIR = "trained_models"
MODEL_PATH = os.path.join(MODEL_DIR, "logistic_regression_gd.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "logistic_standardizer.pkl")

FEATURE_VIEW_FRAUD_V1 = "feature_view_fraud_v1"
FEATURE_VIEW_FRAUD_V2 = "feature_view_fraud_v2"
MODEL_NAME = "logistic_regression_gd"


# LOG TRAINING RUN
def log_training_run(feature_view, model_name, loss, precision_v, recall_v):
    sql = """
        INSERT INTO training_runs
        (feature_view, model_name, loss, precision, recall)
        VALUES
        (:feature_view, :model_name, :loss, :precision, :recall)
    """

    with engine.begin() as conn:
        conn.execute(
            text(sql),
            {
                "feature_view": feature_view,
                "model_name": model_name,
                "loss": float(loss),          # use F1 as loss indicator
                "precision": float(precision_v),   # store precision
                "recall": float(recall_v),  # store recall
            },
        )


# TRAIN
def train():

    print("Loading data from feature view...")
    X, y = load_feature_view(FEATURE_VIEW_FRAUD_V1)
    # X, y = load_feature_view(FEATURE_VIEW_FRAUD_V2)

    print("Splitting data...")
    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)

    print("Standardizing features...")
    X_train, mean, std = standardize(X_train)
    X_val, _, _ = standardize(X_val, mean, std)
    X_test, _, _ = standardize(X_test, mean, std)

    print("Training logistic regression (from scratch)...")
    model = LogisticRegressionGD(lr=0.05, epochs=200)
    model.fit(X_train, y_train)

    print("\nEvaluating on validation set...")
    y_val_pred = model.predict(X_val)

    acc = accuracy(y_val, y_val_pred)
    prec = precision(y_val, y_val_pred)
    rec = recall(y_val, y_val_pred)
    f1 = f1_score(y_val, y_val_pred)

    print("Validation Metrics")
    print("Accuracy :", acc)
    print("Precision:", prec)
    print("Recall   :", rec)
    print("F1 Score :", f1)

    print("Fraud ratio:", sum(y)/len(y))

    # Log experiment
    log_training_run(
        FEATURE_VIEW_FRAUD_V1,
        # FEATURE_VIEW_FRAUD_V2,
        MODEL_NAME,
        f1,     # use F1 as main performance metric
        prec,
        rec,
    )

    print("\nSaving model + scaler...")
    os.makedirs(MODEL_DIR, exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump((mean, std), f)

    print(f"Model saved -> {MODEL_PATH}")
    print(f"Scaler saved -> {SCALER_PATH}")


if __name__ == "__main__":
    train()
