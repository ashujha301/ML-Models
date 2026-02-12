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
    version TEXT,
    path TEXT,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

TRAINING_RUNS_LOGS_SQL = """

CREATE TABLE IF NOT EXISTS training_runs (
    id SERIAL PRIMARY KEY,
    model_version TEXT,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1 FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

INFERENCE_LOGS = """

CREATE TABLE IF NOT EXISTS inference_logs (
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

    model_version TEXT,
    loan_id TEXT,

    prediction INT,
    probability FLOAT,
    reason TEXT,

    age FLOAT,
    income FLOAT,
    credit_score FLOAT,
    loan_amount FLOAT,

    latency_ms FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


"""

DRIFT_EVENTS = """

CREATE TABLE IF NOT EXISTS drift_events (
    id SERIAL PRIMARY KEY,
    model_version TEXT,
    feature_name TEXT,
    current_mean FLOAT,
    baseline_mean FLOAT,
    drift_score FLOAT,
    threshold FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


"""