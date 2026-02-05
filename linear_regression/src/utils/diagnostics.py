def residual_diagnostics(y_true, y_pred):
    residuals = y_true - y_pred
    return {
        "mean_residual": residuals.mean(),
        "std_residual": residuals.std(),
    }
