import pandas as pd
from sqlalchemy import text
from data.db.db_config import engine

CSV_PATH = "data/raw/fraudTest.csv"
TABLE_NAME= "fraud_test_raw"

def load_csv_to_db():
    df = pd.read_csv(CSV_PATH)

    print(f"CSV loaded with shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"DATA Successfully loaded into table: {TABLE_NAME}")

    with engine.begin() as conn:
        res = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
        print("Row count in db: ", res.fetchone()[0])


if __name__ == "__main__":
    load_csv_to_db()