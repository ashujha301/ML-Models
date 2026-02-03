import numpy as np
from src.models.maths import mean_squared_error, compute_gradients

class Linear_RegressionGD:
    """
    Linear regression using Gradient descent
    """

    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs

        self.weights = None
        self.bias = None
        self.loss_history = []

    def _initialize_parameters(self, n_features: int):
        self.weights = np.zeros(n_features)
        self.bias = 0.0

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        y = Xw + b
        """

        return np.dot(X, self.weights) + self.bias
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        n_samples, n_features = X.shape
        self._initialize_parameters(n_features)

        for epoch in range(self.epochs):
            y_pred = self.predict(X)

            loss = mean_squared_error(y, y_pred)
            self.loss_history.append(loss)

            dw, db = compute_gradients(X, y, y_pred)

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db

            if epoch % 100 == 0:
                print(f"Epoch {epoch} | Loss: {loss: .6f}")

        return self