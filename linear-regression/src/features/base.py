import numpy as np

def standardize( X, mean=None, std=None ):
    """
    Standardize features.
    If mean/std are provided, use them (inference).
    Otherwise compute from data (training).
    
    """

    if mean is None:
        mean = X.mean(axis=0)
        
    if std is None:
        std = X.std(axis=0) + 1e-8

    x_scaled = ( X- mean )/std

    return x_scaled, mean, std