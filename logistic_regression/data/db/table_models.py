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

TRAINING_RUNS_LOGS_SQL = """

CREATE TABLE IF NOT EXISTS training_runs (
    run_id SERIAL PRIMARY KEY,
    feature_view TEXT NOT NULL,
    model_name TEXT NOT NULL,
    loss FLOAT,
    precision FLOAT,
    recall FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

INFERENCE_LOGS = """

CREATE TABLE inference_logs (
    id BIGSERIAL PRIMARY KEY,
    
    batch_id UUID,

    model_name TEXT,
    model_version TEXT,
    feature_view TEXT,

    transaction_id TEXT,
    prediction INT,
    probability FLOAT,

    confidence FLOAT,
    drift_detected BOOLEAN,

    amount FLOAT,
    hour INT,
    category_code INT,

    latency_ms FLOAT,

    raw_payload JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


"""