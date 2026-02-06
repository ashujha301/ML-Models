import numpy as np

def detect_drift(x_scaled: np.ndarray, threshold=2):
    """
    Simple drift detection:
    If any feature > threshold std → drift warning
    """
    drift_flags = np.abs(x_scaled) > threshold
    return bool(np.any(drift_flags))
