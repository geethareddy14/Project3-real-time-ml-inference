from fastapi import FastAPI
import numpy as np

from apps.schemas import PredictRequest, PredictResponse
from apps.model_loader import ModelWrapper
from apps.utils import timer_ms

app = FastAPI(title="Real-Time ML Inference API", version="1.0.0")

# Load model on startup (typical production pattern)
model = None

@app.on_event("startup")
def load_model():
    global model
    model = ModelWrapper()
    print("✅ Model loaded successfully")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    global model

    # Feature engineering for inference (must match training logic)
    log_amount = np.log1p(req.amount)
    velocity_ratio = (req.txn_velocity_1h + 1) / (req.txn_velocity_24h + 1)
    is_night = 1 if req.txn_hour in [0, 1, 2, 3, 4, 23] else 0
    new_account_flag = 1 if req.acct_age_days < 180 else 0
    far_geo_flag = 1 if req.geo_distance_km > 120 else 0

    # Keep order consistent with model training FEATURE_COLS
    features = np.array([[
        req.amount,
        log_amount,
        req.txn_hour,
        15,  # txn_day placeholder (if not used, remove from training too)
        req.acct_age_days,
        req.txn_velocity_1h,
        req.txn_velocity_24h,
        velocity_ratio,
        req.geo_distance_km,
        req.device_change_flag,
        is_night,
        new_account_flag,
        far_geo_flag
    ]], dtype=float)

    with timer_ms() as elapsed:
        p = model.predict_proba(features)
        pred = 1 if p >= 0.5 else 0
        latency = elapsed()

    return PredictResponse(
        prediction=pred,
        fraud_probability=round(p, 6),
        latency_ms=round(latency, 3),
        model_version="xgb_model.joblib"
    )
