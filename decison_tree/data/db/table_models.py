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

MODELS_REGISTRY = """

CREATE TABLE IF NOT EXISTS model_registry (
    id SERIAL PRIMARY KEY,
    model_name TEXT,
    model_version TEXT,
    model_path TEXT,
    feature_view TEXT,

    is_active BOOLEAN DEFAULT FALSE,

    metrics JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

TRAINING_RUNS_LOGS_SQL = """

CREATE TABLE IF NOT EXISTS training_runs (
    run_id SERIAL PRIMARY KEY,

    model_name TEXT,
    model_version TEXT,
    feature_view TEXT,

    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,

    training_rows INT,
    validation_rows INT,

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

PREDICTION_LOGS = """

CREATE TABLE IF NOT EXISTS prediction_logs (
    id SERIAL PRIMARY KEY,

    model_name TEXT,
    model_version TEXT,
    feature_view TEXT,

    input_data JSONB,

    prediction INT,
    confidence FLOAT,

    latency_ms FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


"""

DRIFT_EVENTS = """

CREATE TABLE IF NOT EXISTS drift_events (
    id SERIAL PRIMARY KEY,

    model_version TEXT,
    feature_name TEXT,

    drift_score FLOAT,
    threshold FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


"""