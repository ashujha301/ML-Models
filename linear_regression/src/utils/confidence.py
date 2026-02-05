import numpy as np

def compute_confidence(x_scaled: np.ndarray):
    """
    Confidence based on distance from training distribution.
    If features are far from mean → low confidence.
    """

    # z-score distance
    z = np.abs(x_scaled)

    mean_z = np.mean(z)

    # heuristic: beyond 3 std → very low confidence
    confidence = max(0.0, 1 - (mean_z / 3))

    return round(float(confidence), 3)
