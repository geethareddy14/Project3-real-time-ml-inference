from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    # Keep fields aligned with Project 2 feature schema.
    # You can start with a small subset and expand later.
    amount: float = Field(..., ge=0)
    txn_hour: int = Field(..., ge=0, le=23)
    acct_age_days: int = Field(..., ge=0)
    txn_velocity_1h: int = Field(..., ge=0)
    txn_velocity_24h: int = Field(..., ge=0)
    geo_distance_km: float = Field(..., ge=0)
    device_change_flag: int = Field(..., ge=0, le=1)

class PredictResponse(BaseModel):
    prediction: int
    fraud_probability: float
    latency_ms: float
    model_version: str
