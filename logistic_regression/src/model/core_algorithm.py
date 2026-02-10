import numpy as np
from src.model.maths import sigmoid, binary_cross_entropy, compute_gradients

class LogisticRegressionGD:

    def __init__(self, lr=0.01, epochs=600):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = 0

    def fit(self, X, y):

        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)

        for epoch in range(self.epochs):

            linear = np.dot(X, self.weights) + self.bias
            y_pred = sigmoid(linear)

            loss = binary_cross_entropy(y, y_pred)

            dw, db = compute_gradients(X, y, y_pred)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

            if epoch % 20 == 0:
                print(f"Epoch {epoch} | Loss {loss:.6f}")

    def predict_proba(self, X):
        linear = np.dot(X, self.weights) + self.bias
        return sigmoid(linear)

    def predict(self, X, threshold=0.3):
        probs = self.predict_proba(X)
        return (probs >= threshold).astype(int)
