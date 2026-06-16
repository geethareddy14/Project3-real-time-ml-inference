import os
import logging
import joblib
import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")

class DummyModel:
    """Fallback model when no trained artifact is present."""
    def predict_proba(self, X):
        amount = X[0, 0]
        hour = X[0, 1]
        distance = X[0, 2]
        device_change = X[0, 3]

        score = 0.0
        score += 0.35 if amount > 200 else 0.05
        score += 0.25 if hour in [0, 1, 2, 3, 4, 23] else 0.05
        score += 0.25 if distance > 120 else 0.05
        score += 0.20 if device_change == 1 else 0.05

        p = min(max(score, 0.01), 0.95)
        return np.array([[1 - p, p]])

class ModelWrapper:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH):
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.version = os.path.basename(self.model_path)
                logger.info(f"Loaded model from {self.model_path}")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Using DummyModel.")
                self.model = DummyModel()
                self.version = "dummy-fallback"
        else:
            logger.warning(f"Model not found at {self.model_path}. Using DummyModel.")
            self.model = DummyModel()
            self.version = "dummy-fallback"

    def predict_proba(self, features_2d: np.ndarray) -> float:
        try:
            proba = self.model.predict_proba(features_2d)
            return float(proba[0, 1])
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise