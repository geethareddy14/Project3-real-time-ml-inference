# Project 3 — Real-Time ML Inference API (FastAPI)

A production-style model serving service that exposes a `/predict` endpoint for real-time fraud/risk scoring.

## What it demonstrates
- Model loading at startup
- Request validation (Pydantic)
- Feature engineering at inference time (train/inference parity)
- Low-latency scoring + latency reporting
- Dockerized deployment

## Run
1) Place your model:
- `models/xgb_model.joblib` (copy from Project 2)

2) Start API:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
