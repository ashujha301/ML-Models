import numpy as np

def gini_from_counts(left_counts, right_counts):
    left_total = left_counts.sum()
    right_total = right_counts.sum()

    if left_total == 0 or right_total == 0:
        return 1e9

    left_prob = left_counts / left_total
    right_prob = right_counts / right_total

    g_left = 1 - np.sum(left_prob**2)
    g_right = 1 - np.sum(right_prob**2)

    return (left_total * g_left + right_total * g_right) / (left_total + right_total)


def best_split(X, y):

    n_samples, n_features = X.shape
    best_feature = None
    best_threshold = None
    best_gini = 1e9

    classes = np.unique(y)

    for feature in range(n_features):

        # sort feature
        sorted_idx = np.argsort(X[:, feature])
        X_sorted = X[sorted_idx]
        y_sorted = y[sorted_idx]

        # class counts
        right_counts = np.array([np.sum(y_sorted == c) for c in classes])
        left_counts = np.zeros_like(right_counts)

        for i in range(1, n_samples):

            c = y_sorted[i-1]
            class_idx = np.where(classes == c)[0][0]

            left_counts[class_idx] += 1
            right_counts[class_idx] -= 1

            # skip identical values
            if X_sorted[i, feature] == X_sorted[i-1, feature]:
                continue

            g = gini_from_counts(left_counts, right_counts)

            if g < best_gini:
                best_gini = g
                best_feature = feature
                best_threshold = (X_sorted[i, feature] + X_sorted[i-1, feature]) / 2

    return best_feature, best_threshold, best_gini
