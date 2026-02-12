import os
import pickle
import uuid
from sqlalchemy import text

from data.db.db_config import engine
from src.training.data_loader import load_feature_view
from src.training.split import train_val_test_split
from src.model.core_algorithm import DecisionTreeClassifierScratch
from src.training.metrics import accuracy, precision, recall, f1_score

FEATURE_VIEW = "feature_view_loan_v1"
MODEL_NAME = "decision_tree"
MODEL_DIR = "trained_models"

def register_model(version, path):
    sql = """
    INSERT INTO model_registry (model_name, version, path, is_active)
    VALUES (:name, :version, :path, TRUE)
    """

    deactivate = """
    UPDATE model_registry
    SET is_active = FALSE
    WHERE model_name = :name
    """

    with engine.begin() as conn:
        conn.execute(text(deactivate), {"name": MODEL_NAME})
        conn.execute(text(sql), {
            "name": MODEL_NAME,
            "version": version,
            "path": path
        })


def log_training(version, acc, prec, rec, f1s):
    sql = """
    INSERT INTO training_runs
    (model_version, accuracy, precision, recall, f1)
    VALUES (:v, :a, :p, :r, :f)
    """

    with engine.begin() as conn:
        conn.execute(text(sql), {
            "v": version,
            "a": float(acc),
            "p": float(prec),
            "r": float(rec),
            "f": float(f1s)
        })


def train():

    print("Loading data...")
    X, y = load_feature_view(FEATURE_VIEW)

    X_train, y_train, X_val, y_val, X_test, y_test = train_val_test_split(X, y)

    print("Training tree...")
    model = DecisionTreeClassifierScratch(max_depth=6)
    model.fit(X_train, y_train)

    print("Evaluating...")
    pred = model.predict(X_val)

    acc = accuracy(y_val, pred)
    prec = precision(y_val, pred)
    rec = recall(y_val, pred)
    f1s = f1_score(y_val, pred)

    print("ACC:", acc)
    print("PREC:", prec)
    print("REC:", rec)
    print("F1:", f1s)

    version = str(uuid.uuid4())[:8]
    os.makedirs(MODEL_DIR, exist_ok=True)

    path = f"{MODEL_DIR}/tree_{version}.pkl"

    with open(path, "wb") as f:
        pickle.dump(model, f)

    register_model(version, path)
    log_training(version, acc, prec, rec, f1s)

    print("Model saved:", version)


if __name__ == "__main__":
    train()
