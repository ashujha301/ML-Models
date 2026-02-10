import pickle
import os

MODEL_PATH = "trained_models/logistic_regression_gd.pkl"
SCALER_PATH = "trained_models/logistic_standardizer.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(SCALER_PATH, "rb") as f:
        mean, std = pickle.load(f)

    return model, mean, std
