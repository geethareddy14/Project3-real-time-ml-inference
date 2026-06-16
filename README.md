# Project 3 — Real-Time ML Inference API (FastAPI)

A production-style model serving service that exposes a `/predict` endpoint for real-time fraud/risk scoring.

## What it demonstrates
- API-first model serving (FastAPI)
- Request validation (Pydantic)
- Model loading on startup
- Low-latency scoring + latency response
- Dockerized deployment

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
