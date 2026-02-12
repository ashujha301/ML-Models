from prometheus_client import Counter, Histogram, Gauge

# total predictions
PREDICTION_COUNT = Counter(
    "loan_predictions_total",
    "Total predictions made"
)

# approvals
APPROVAL_COUNT = Counter(
    "loan_approvals_total",
    "Total approved loans"
)

# latency
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds",
    "Time spent on prediction"
)

# drift metric
DRIFT_SCORE = Gauge(
    "feature_drift_score",
    "Drift score of latest request"
)
