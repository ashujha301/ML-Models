from data.db.db_config import engine
from data.db.table_models import ( FEATURE_VIEW_REGISTRY_SQL, FEATURE_REGISTRY_SQL, TRAINING_RUNS_LOGS_SQL, INFERENCE_LOGS)
from sqlalchemy import text

def init_feature_tables():
    with engine.begin() as conn:
        conn.execute(text(FEATURE_REGISTRY_SQL))
        conn.execute(text(FEATURE_VIEW_REGISTRY_SQL))
        conn.execute(text(TRAINING_RUNS_LOGS_SQL))
        conn.execute(text(INFERENCE_LOGS))

        print(f"Tables created successfully--->")


if __name__ == "__main__":
    init_feature_tables()