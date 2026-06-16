# Project 3 — Real-Time ML Inference API (FastAPI)

A production-grade real-time fraud detection inference service built with FastAPI, designed for low-latency scoring, batch processing, and enterprise-ready observability.

---

## Overview

This project implements a **real-time ML inference API** that scores financial transactions for fraud risk. It exposes REST endpoints for single and batch predictions, includes a health monitoring endpoint, and is fully containerized with Docker for production deployment.

The service is built around a `ModelWrapper` class that gracefully handles missing model artifacts using a rule-based `DummyModel` fallback — ensuring the API stays live even without a trained artifact present.

---

## Architecture

```
Client Request
      │
      ▼
 FastAPI App (lifespan handler)
      │
      ├── /predict        → Single transaction scoring
      ├── /predict/batch  → Batch transaction scoring
      ├── /health         → Service health + uptime
      └── /model/info     → Model metadata
      │
      ▼
 ModelWrapper
      ├── Loads joblib model artifact (if present)
      └── Falls back to DummyModel (rule-based scoring)
      │
      ▼
 PredictResponse
      ├── fraud_probability (float)
      ├── risk_level (LOW / MEDIUM / HIGH)
      ├── latency_ms
      └── request_id (UUID)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI 0.110+ |
| Data Validation | Pydantic v2 |
| ML Runtime | scikit-learn / joblib |
| Numerical Computing | NumPy |
| Logging | Python logging (structured) |
| Containerization | Docker |
| Server | Uvicorn (ASGI) |

---

## API Endpoints

### `POST /predict`
Score a single transaction for fraud risk.

**Request:**
```json
{
  "amount": 450.00,
  "txn_hour": 2,
  "geo_distance_km": 180.0,
  "device_change_flag": 1
}
```

**Response:**
```json
{
  "request_id": "a1b2c3d4-...",
  "prediction": 1,
  "fraud_probability": 0.87,
  "risk_level": "HIGH",
  "latency_ms": 3.2,
  "model_version": "model.joblib",
  "timestamp": "2026-06-15T13:35:00"
}
```

---

### `POST /predict/batch`
Score multiple transactions in a single call.

**Request:**
```json
{
  "transactions": [
    { "amount": 50.0, "txn_hour": 14, "geo_distance_km": 5.0, "device_change_flag": 0 },
    { "amount": 900.0, "txn_hour": 3, "geo_distance_km": 250.0, "device_change_flag": 1 }
  ]
}
```

**Response:**
```json
{
  "results": [...],
  "total_processed": 2,
  "high_risk_count": 1,
  "processing_time_ms": 7.4
}
```

---

### `GET /health`
Returns service health, model load status, and uptime.

```json
{
  "status": "healthy",
  "model_version": "model.joblib",
  "model_loaded": true,
  "uptime_seconds": 3600,
  "timestamp": "2026-06-15T14:00:00"
}
```

---

### `GET /model/info`
Returns metadata about the currently loaded model.

---

## Risk Classification

| Risk Level | Fraud Probability |
|---|---|
| LOW | < 0.30 |
| MEDIUM | 0.30 – 0.70 |
| HIGH | > 0.70 |

---

## Key Features

- **Lifespan handler** — Model loads once at startup, not per request
- **Request ID tracking** — Every prediction gets a UUID for traceability
- **Batch scoring** — Process multiple transactions with aggregate stats
- **Graceful fallback** — Rule-based DummyModel activates when no artifact found
- **Structured logging** — Timestamped logs for every prediction and error
- **Latency tracking** — Response time included in every prediction result
- **Pydantic validation** — Input constraints enforced at the schema level

---

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload --port 8000
```

Open Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Run with Docker

```bash
# Build the image
docker build -t real-time-ml-inference .

# Run the container
docker run -p 8000:8000 real-time-ml-inference
```

---

## Project Structure

```
Project3-real-time-ml-inference/
├── app/
│   ├── main.py           # FastAPI app, endpoints, lifespan handler
│   ├── model_loader.py   # ModelWrapper + DummyModel fallback
│   ├── schemas.py        # Pydantic request/response models
│   └── utils.py          # Timer and risk level utilities
├── models/               # Trained model artifacts (.joblib)
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Use Case

This service is designed for **real-time fraud detection** in financial transaction pipelines. It can be deployed as a microservice behind an API gateway, integrated with streaming platforms like Kafka or Kinesis, or called directly from payment processing systems requiring sub-10ms scoring latency.