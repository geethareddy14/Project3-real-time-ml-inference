import os
import joblib

DEFAULT_MODEL_PATH = os.getenv("MODEL_PATH", "models/xgb_model.joblib")

class ModelWrapper:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model not found at '{model_path}'. "
                f"Place your model at models/xgb_model.joblib or set MODEL_PATH."
            )
        self.model_path = model_path
        self.model = joblib.load(model_path)

    def predict_proba(self, features_2d):
        # XGBoost sklearn API supports predict_proba
        proba = self.model.predict_proba(features_2d)[:, 1]
        return float(proba[0])
