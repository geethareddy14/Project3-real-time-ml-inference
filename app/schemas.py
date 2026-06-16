from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    amount: float = Field(..., ge=0, description="Transaction amount in USD")
    txn_hour: int = Field(..., ge=0, le=23, description="Hour of transaction (0-23)")
    geo_distance_km: float = Field(..., ge=0, description="Geographic distance from home in km")
    device_change_flag: int = Field(..., ge=0, le=1, description="1 if device changed since last transaction")

class PredictResponse(BaseModel):
    request_id: str
    prediction: int
    fraud_probability: float
    risk_level: str
    latency_ms: float
    model_version: str
    timestamp: str

class BatchRequest(BaseModel):
    transactions: List[PredictRequest]

class BatchResponse(BaseModel):
    results: List[PredictResponse]
    total_processed: int
    high_risk_count: int
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    model_version: str
    model_loaded: bool
    uptime_seconds: int
    timestamp: str