# Payment Webhook System

A production-ready webhook processing system built using entity["software","FastAPI",""] and entity["software","PostgreSQL",""].

This project supports:

* Secure webhook signature validation
* Duplicate webhook protection (Idempotency)
* Single webhook processing
* Bulk webhook processing
* Structured logging
* Repository-Service architecture
* Alembic database migrations
* Enterprise-ready scalable code structure

---

# Project Structure

```bash
payment_webhook_system/
│
├── alembic/
├── app/
│   ├── api/
│   │   ├── public/
│   │   └── private/
│   │
│   ├── core/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── tests/
│   └── utils/
│
├── logs/
├── mock_payloads/
├── .env
├── requirements.txt
└── README.md
```

---

# Features

## Webhook Signature Verification

Uses HMAC SHA256 signature validation.

## Duplicate Webhook Protection

Prevents duplicate event processing using unique event IDs.

## Bulk Webhook Processing

Supports processing multiple webhook payloads in a single request.

## Structured Logging

All webhook requests and responses are logged.

## Clean Enterprise Architecture

Uses:

* Router Layer
* Service Layer
* Repository Layer
* Utility Layer
* Exception Layer

---

# Tech Stack

* Python 3.12+
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Uvicorn

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/shivam-kumar-sain/payment_webhook_system.git
```

```bash
cd payment_webhook_system
```

---

# 2. Create Virtual Environment

## Windows

```bash
py -m venv civic_venv
```

Activate:

```bash
civic_venv\Scripts\activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Configure Environment Variables

Create `.env`

```env
APP_NAME=Payment Webhook System
APP_VERSION=1.0.0
APP_TITLE=Payment Webhook API

DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=payment_webhook_system_db

WEBHOOK_SECRET=test_secret

JWT_SECRET=secret_key

SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

---

# 5. Create PostgreSQL Database

Open PostgreSQL and create database:

```sql
CREATE DATABASE payment_webhook_system_db;
```

---

# 6. Run Database Migration

## Create Migration

```bash
alembic revision --autogenerate -m "initial migration"
```

## Apply Migration

```bash
alembic upgrade head
```

---

# 7. Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

Server:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

# Webhook API

## Single Webhook

### Endpoint

```http
POST /webhook/payments
```

### Example Payload

```json
{
  "event": "payment.authorized",
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_001",
        "status": "authorized",
        "amount": 1000,
        "currency": "INR"
      }
    }
  },
  "created_at": 1751885965,
  "id": "evt_auth_001"
}
```

---

# Bulk Webhook

## Example Payload

```json
[
  {
    "event": "payment.authorized",
    "payload": {
      "payment": {
        "entity": {
          "id": "pay_001",
          "status": "authorized",
          "amount": 1000,
          "currency": "INR"
        }
      }
    },
    "created_at": 1751885965,
    "id": "evt_auth_001"
  },
  {
    "event": "payment.authorized",
    "payload": {
      "payment": {
        "entity": {
          "id": "pay_002",
          "status": "authorized",
          "amount": 5000,
          "currency": "INR"
        }
      }
    },
    "created_at": 1751886265,
    "id": "evt_auth_002"
  }
]
```

---

# Testing Webhooks

## Using CURL

```bash
curl -X POST http://127.0.0.1:8000/webhook/payments \
-H "Content-Type: application/json" \
-H "X-Razorpay-Signature: TEST_SIGNATURE" \
-d @mock_payloads/payment_authorized.json
```

---

# Python Test Script

Run:

```bash
py app/tests/test_webhook.py
```

---

# Logging

Webhook logs are stored in:

```text
logs/webhook_test_logs.json
```

---

# Duplicate Webhook Handling

If the same event ID is received again:

```json
{
  "status": false,
  "message": "Duplicate webhook event"
}
```

---

# Signature Validation

Uses:

```text
HMAC SHA256
```

Header:

```http
X-Razorpay-Signature
```

---

# API Response Example

```json
{
  "status": true,
  "message": "Webhook processed successfully",
  "data": {
    "event_id": "evt_auth_001",
    "payment_id": "pay_001",
    "event_type": "payment.authorized"
  }
}
```

---

# Future Improvements

* Redis Queue Support
* Celery Background Workers
* Kafka Integration
* Retry Mechanism
* Dead Letter Queue
* Rate Limiting
* Webhook Replay System
* Docker Support
* CI/CD Pipeline
* Unit Testing

---

# Author

Shivam Kumar
