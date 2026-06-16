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
```

## Project Overview
This repository provides a real-time ML inference service built with FastAPI and Docker.

## Architecture
- Data ingestion and request validation
- Model loading and caching on startup
- Real-time scoring via `/predict`
- Latency tracking in response payload

## Tech Stack
- Python
- FastAPI
- Pydantic
- Docker

## Repository Structure
- `app/` — application package
- `app/main.py` — FastAPI app and endpoints
- `app/model_loader.py` — model loading logic
- `app/schemas.py` — request/response schemas
- `app/utils.py` — helper utilities
- `requirements.txt` — Python dependencies

## Notes
Update this README with model-specific metrics, problem statement details, and deployment instructions as the project evolves.

