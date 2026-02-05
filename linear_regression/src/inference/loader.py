import pickle

MODEL_PATH = "models/linear_regression_gd.pkl"
SCALER_PATH = "models/standardizer.pkl"


def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def load_scaler():
    with open(SCALER_PATH, "rb") as f:
        return pickle.load(f)
