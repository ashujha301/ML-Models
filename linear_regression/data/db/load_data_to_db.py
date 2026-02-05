import pandas as pd 
from sqlalchemy import text
from data.db.db_config import engine


# CSV_PATH = "data/raw/marketing_campaign_dataset.csv"
# TABLE_NAME= "marketing_campaign_raw"
CSV_PATH = "data/raw/housing.csv"
TABLE_NAME= "housing_raw"

def load_csv_to_db():
    df = pd.read_csv(CSV_PATH)

    print(f"CSV Loaded with shape: {df.shape}")
    print(f"Columns:", list(df.columns))

    df.to_sql(
        TABLE_NAME,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Data Successfully loaded into table: {TABLE_NAME}")

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
        print("Row count in db:", result.fetchone()[0])

if __name__ == "__main__":
    load_csv_to_db()