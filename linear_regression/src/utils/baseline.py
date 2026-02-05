import numpy as np

def mean_baseline(y_train, size):
    return np.full(size, np.mean(y_train))
