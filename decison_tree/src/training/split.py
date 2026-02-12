import numpy as np

def train_val_test_split(X, y, train_ratio=0.7, val_ratio=0.15):
    n = X.shape[0]
    indices = np.random.permutation(n)

    train_end = int(train_ratio * n)
    val_end = train_end + int(val_ratio *n)

    train_idx = indices[:train_end]
    val_idx = indices[train_end:val_end]
    test_idx = indices[val_end:]

    return ( X[train_idx], y[train_idx], X[val_idx], y[val_idx], X[test_idx], y[test_idx])