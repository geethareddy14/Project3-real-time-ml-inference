import uuid
import logging
from contextlib import asynccontextmanager
from datetime import datetime

import numpy as np
from fastapi import FastAPI, HTTPException

from app.schemas import PredictRequest, PredictResponse, BatchRequest, BatchResponse, HealthResponse
from app.model_loader import ModelWrapper
from app.utils import timer_ms, get_risk_level

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

model: ModelWrapper = None
startup_time: datetime = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, startup_time
    model = ModelWrapper()
    startup_time = datetime.utcnow()
    logger.info(f"Model loaded: {model.version}")
    yield
    logger.info("Shutting down")

app = FastAPI(
    title="Real-Time ML Inference API",
    description="Production-grade real-time fraud detection inference service",
    version="2.0.0",
    lifespan=lifespan
)

@app.get("/health", response_model=HealthResponse)
def health():
    uptime = (datetime.utcnow() - startup_time).seconds if startup_time else 0
    return HealthResponse(
        status="healthy",
        model_version=model.version if model else "not loaded",
        model_loaded=model is not None,
        uptime_seconds=uptime,
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/model/info")
def model_info():
    return {
        "model_version": model.version if model else "not loaded",
        "model_type": type(model.model).__name__