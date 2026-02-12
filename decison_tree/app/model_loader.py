import pickle
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
        raise Exception("No active model")

    version, path = row

    with open(path, "rb") as f:
        model = pickle.load(f)

    print("Loaded model:", version)
