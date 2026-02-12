import numpy as np
from src.model.core_algorithm import DecisionTreeClassifierScratch

X = np.array([
    [25, 50000],
    [45, 80000],
    [22, 20000],
    [35, 120000],
    [52, 150000],
])

y = np.array([0,1,0,1,1])

tree = DecisionTreeClassifierScratch(max_depth=3)
tree.fit(X,y)

pred = tree.predict(X)

print("Pred:", pred)
