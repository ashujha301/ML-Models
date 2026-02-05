def detect_feature_drift( train_stats, current_stats, threshold=0.2):

    for feature in train_stats:
        shift = abs(current_stats[feature]["mean"] - train_stats[feature]["mean"])

        if shift > threshold:
            print(f" DRIFT detected in {feature}")