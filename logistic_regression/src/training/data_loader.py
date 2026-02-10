import pandas as pd
from data.db.db_config import engine

def load_feature_view(feature_view_name: str):
    df = pd.read_sql(f"SELECT * FROM {feature_view_name}", con=engine)

    X = df.drop(columns=["target"]).values
    y = df["target"].values

    return X, y