import numpy as np 

def gini(y):
    """
    Gini = 1 - sum(p^2)
    
    """

    if len(y) == 0:
        return 0

    p1 = np.sum( y == 1)/ len(y)
    p0 = 1 - p1

    return 1 - (p1**2 + p0**2)


def split_dataset(X, y, feature_index, threshold):

    left_mask = X[:, feature_index] <= threshold
    right_mask = X[:, feature_index] > threshold

    X_left, y_left = X[left_mask], y[left_mask]
    X_right, y_right = X[right_mask], y[right_mask]

    return X_left, y_left, X_right, y_right



def best_split(X, y):

    best_feature = None
    best_threshold = None
    best_gini = 1.0

    n_samples, n_features = X.shape

    for feature in range(n_features):

        thresholds = np.unique(X[:, feature])

        for t in thresholds:

            X_l, y_l, X_r, y_r = split_dataset(X, y, feature, t)

            if len(y_l) == 0 or len(y_r) == 0:
                continue

            g = (
                (len(y_l)/n_samples) * gini(y_l) +
                (len(y_r)/n_samples) * gini(y_r)
            )

            if g < best_gini:
                best_gini = g
                best_feature = feature
                best_threshold = t

    return best_feature, best_threshold, best_gini