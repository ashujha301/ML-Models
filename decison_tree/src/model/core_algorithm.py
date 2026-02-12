import numpy as np
from src.model.maths import best_split


class Node:
    def __init__(self,
                 feature=None,
                 threshold=None,
                 left=None,
                 right=None,
                 value=None):

        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value


class DecisionTreeClassifierScratch:

    def __init__(self,
                 max_depth=5,
                 min_samples_split=10):

        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None



    def fit(self, X, y):
        self.root = self._grow_tree(X, y, depth=0)


    def _grow_tree(self, X, y, depth):

        num_samples = X.shape[0]
        num_labels = len(np.unique(y))

        # stopping conditions
        if (
            depth >= self.max_depth
            or num_labels == 1
            or num_samples < self.min_samples_split
        ):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        # find best split
        feature, threshold, g = best_split(X, y)

        if feature is None:
            return Node(value=self._most_common_label(y))

        # split
        left_mask = X[:, feature] <= threshold
        right_mask = X[:, feature] > threshold

        left = self._grow_tree(X[left_mask], y[left_mask], depth+1)
        right = self._grow_tree(X[right_mask], y[right_mask], depth+1)

        return Node(feature, threshold, left, right)


    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])


    def _traverse_tree(self, x, node):

        if node.value is not None:
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)

        return self._traverse_tree(x, node.right)


    def _most_common_label(self, y):
        return np.bincount(y.astype(int)).argmax()
