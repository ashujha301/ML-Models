def confidence_score( x, mean, std):
    z = abs( x- mean) / std

    return max(0, 1-z)
