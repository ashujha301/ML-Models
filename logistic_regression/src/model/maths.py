import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def binary_cross_entropy(y, y_pred):
    eps = 1e-9

    return np.mean(y*np.log(y_pred + eps) + (1 -y)*np.log(1 - y_pred + eps))

def compute_gradients(X, y, y_pred):
    n = X.shape[0]
    fraud_weight = 5
    weights = np.where(y == 1, fraud_weight, 1)
    err = (y_pred - y) * weights

    dw = (1/n)*np.dot(X.T, err)
    db = (1/n) * np.sum(err)

    return dw, db

