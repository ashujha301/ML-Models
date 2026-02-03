from data.db.db_config import engine
from data.db.table_models import ( FEATURE_VIEW_REGISTRY_SQL, FEATURE_REGISTRY_SQL )
from sqlalchemy import text

def init_feature_tables():
    with engine.begin() as conn:
        conn.execute(text(FEATURE_REGISTRY_SQL))
        conn.execute(text(FEATURE_VIEW_REGISTRY_SQL))

        print("Feature registry tables created successfully")


if __name__ == "__main__":
    init_feature_tables()