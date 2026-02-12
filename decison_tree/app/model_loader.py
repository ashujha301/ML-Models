import pickle
import threading
import time
from sqlalchemy import text
from data.db.db_config import engine

model = None
version = None


def load_active_model():
    global model, version

    sql = """
    SELECT version, path
    FROM model_registry
    WHERE is_active = TRUE
    LIMIT 1
    """

    with engine.begin() as conn:
        row = conn.execute(text(sql)).fetchone()

    if row is None:
        raise Exception("No active model found")

    db_version, path = row

    with open(path, "rb") as f:
        loaded_model = pickle.load(f)

    model = loaded_model
    version = db_version

    print(f"Loaded model version: {version}")

#watch for new model and reload
def watch_for_new_model(interval=20):
    global model, version

    while True:
        time.sleep(interval)

        sql = """
        SELECT version, path
        FROM model_registry
        WHERE is_active = TRUE
        LIMIT 1
        """

        with engine.begin() as conn:
            row = conn.execute(text(sql)).fetchone()

        if row is None:
            continue

        db_version, path = row

        if db_version != version:
            print("New model detected → reloading")

            with open(path, "rb") as f:
                new_model = pickle.load(f)

            model = new_model
            version = db_version

            print("Model switched to:", version)
