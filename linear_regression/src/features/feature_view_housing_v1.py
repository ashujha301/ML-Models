from sqlalchemy import text
from data.db.db_config import engine
from src.features.registry import register_feature_view, registry_feature

FEATURE_VIEW_NAME = "feature_view_housing_v1"
RAW_TABLE = "housing_raw"
TARGET_COLUMN = "median_house_value"

FEATURE_VIEW_DESCRIPTION = """
Linear regression feature view for housing price prediction.
Strong linear relationships → ideal test for model pipeline.
"""

FEATURES = {
    "median_income": {
        "description": "Median income",
        "data_type": "numeric",
        "source_column": "median_income",
        "transformation": "identity",
    },
    "housing_median_age": {
        "description": "House age",
        "data_type": "numeric",
        "source_column": "housing_median_age",
        "transformation": "identity",
    },
    "total_rooms": {
        "description": "Total rooms",
        "data_type": "numeric",
        "source_column": "total_rooms",
        "transformation": "identity",
    },
    "population": {
        "description": "Population",
        "data_type": "numeric",
        "source_column": "population",
        "transformation": "identity",
    },
    "households": {
        "description": "Households",
        "data_type": "numeric",
        "source_column": "households",
        "transformation": "identity",
    },
    "latitude": {
        "description": "Latitude",
        "data_type": "numeric",
        "source_column": "latitude",
        "transformation": "identity",
    },
    "longitude": {
        "description": "Longitude",
        "data_type": "numeric",
        "source_column": "longitude",
        "transformation": "identity",
    },
}


def create_feature_view():

    register_feature_view(
        feature_view=FEATURE_VIEW_NAME,
        description=FEATURE_VIEW_DESCRIPTION.strip(),
    )

    for name, meta in FEATURES.items():
        registry_feature(
            feature_name=name,
            feature_view=FEATURE_VIEW_NAME,
            description=meta["description"],
            data_type=meta["data_type"],
            source_column=meta["source_column"],
            transformation=meta["transformation"],
        )

    sql = f"""
    CREATE TABLE {FEATURE_VIEW_NAME} AS
    SELECT
        median_income,
        housing_median_age,
        total_rooms,
        population,
        households,
        latitude,
        longitude,
        {TARGET_COLUMN} AS target
    FROM {RAW_TABLE}
    WHERE {TARGET_COLUMN} IS NOT NULL;
    """

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {FEATURE_VIEW_NAME};"))
        conn.execute(text(sql))

    print(f"{FEATURE_VIEW_NAME} created")
    

if __name__ == "__main__":
    create_feature_view()
