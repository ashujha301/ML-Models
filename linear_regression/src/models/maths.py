import numpy as np

#MSE - Cost function 
def mean_squared_error( y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    MSE = ( 1/n )* sum((y_pred - y_true)^2)
    """

    n = y_true.shape[0]
    return (1/n) * np.sum((y_pred - y_true) **2)


# Gradient Descent
def compute_gradients(X: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray):
    """
    Gradient descent w.r.t w and b.
    """

    n = y_true.shape[0]
    error = y_pred - y_true

    dw = (2/n) * np.dot(X.T, error)
    db = (2/n) * np.sum(error)

    return dw, db
