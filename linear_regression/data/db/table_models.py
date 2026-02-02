from sqlalchemy import text

FEATURE_VIEW_REGISTRY_SQL = """

CREATE TABLE IF NOT EXISTS feature_view_registry (
    feature_view TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

FEATURE_REGISTRY_SQL = """

CREATE TABLE IF NOT EXISTS feature_registry (
    feature_name TEXT,
    feature_view TEXT,
    description TEXT NOT NULL,
    data_type TEXT NOT NULL,
    source_column TEXT,
    transformation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ( feature_name, feature_view )
);

"""