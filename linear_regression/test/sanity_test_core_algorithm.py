import numpy as np
from src.models.core_algorithm import Linear_RegressionGD

X = np.array([[1], [2], [3], [4]], dtype=float)
y = np.array([2, 4, 6, 8], dtype=float)

model = Linear_RegressionGD(learning_rate=0.1, epochs=500)
model.fit(X, y)

print("Weights:", model.weights)
print("Bias:", model.bias)