import numpy as np

def validate_prediction_value(y):
    if np.isnan(y) or np.isinf(y):
        raise ValueError("Prediction produced NaN or Inf")

def validate_feature_vector(x):
    if np.any(np.isnan(x)):
        raise ValueError("Input contains NaN")
