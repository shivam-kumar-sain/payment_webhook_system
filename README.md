# 💳 Payment Webhook System

A production-ready webhook processing system built using **FastAPI** and **PostgreSQL**.

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-latest-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✅ Features

- 🔐 **Secure Webhook Signature Validation** — HMAC SHA256
- 🔁 **Duplicate Webhook Protection** — Idempotency via unique event IDs
- 📦 **Single & Bulk Webhook Processing**
- 📋 **Structured Logging** — All requests and responses logged
- 🏗️ **Clean Enterprise Architecture** — Router → Service → Repository → Utility layers
- 🗄️ **Alembic Database Migrations**
- 🐳 **Docker Support**

---

## 🏗️ Project Structure

```bash
PAYMENT_WEBHOOK_SYSTEM/
├── alembic/
│   ├── versions/
│   │   └── 4d69e3e3ab7c_create_payment_events_table.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── private/
│   │   ├── public/
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── database.py
│   │   ├── logger.py
│   │   └── security.py
│   ├── dependencies/
│   │   └── auth_dependency.py
│   ├── exceptions/
│   │   ├── custom_exception.py
│   │   └── handlers.py
│   ├── middleware/
│   │   └── request_logging.py
│   ├── models/
│   │   └── payment_event_model.py
│   ├── repositories/
│   │   └── payment_event_repository.py
│   ├── schemas/
│   │   ├── request/
│   │   │   └── webhook_request_schema.py
│   │   └── response/
│   │       └── payment_response_schema.py
│   ├── services/
│   │   └── payment_webhook_service.py
│   ├── static/
│   │   └── favicon.ico
│   ├── tests/
│   │   ├── test_payment_events.py
│   │   └── test_webhook.py
│   └── utils/
│       ├── datetime_helper.py
│       ├── payload_parser.py
│       └── signature_helper.py
│
├── main.py
├── logs/
│   ├── main.log
│   ├── payment_webhook_service.log
│   └── webhook_test_logs.json
├── mock_payloads/
│   ├── payment_authorized.json
│   ├── payment_captured.json
│   └── payment_failed.json
├── .env
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── DOCS.md
├── README.md
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12+ | Core Language |
| FastAPI | Web Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Database Migrations |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |

---

## 🚀 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/shivam-kumar-sain/payment_webhook_system.git
cd payment_webhook_system
```

### 2. Create Virtual Environment

**Windows:**
```bash
py -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# ===============================
# APP CONFIG
# ===============================
APP_NAME=Payment Webhook System
APP_VERSION=1.0.0
APP_DESCRIPTION=Payment Webhook System Documentation
APP_TITLE=Payment Webhook System API Documentation

# Swagger URLs
DOCS_URL=/docs
REDOC_URL=/redoc
OPENAPI_URL=/openapi.json

# ===============================
# DATABASE CONFIG (PostgreSQL)
# ===============================
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=payment_webhook_system_db

# ===============================
# SECURITY
# ===============================
WEBHOOK_SECRET=your_webhook_secret

# ===============================
# LOGGING
# ===============================
LOG_LEVEL=INFO

# ===============================
# SERVER
# ===============================
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

### 5. Create PostgreSQL Database

```sql
CREATE DATABASE payment_webhook_system_db;
```

### 6. Run Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "initial migration"

# Apply migration
alembic upgrade head
```

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000` | Base Server |
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |

---

## 📡 API Reference

### POST — Single Webhook

```http
POST /webhook/payments
```

**Headers:**
```
Content-Type: application/json
X-Razorpay-Signature: your_webhook_secret
```

**Request Body:**
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

**Success Response:**
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

**Duplicate Event Response:**
```json
{
  "status": false,
  "message": "Duplicate webhook event"
}
```

---

### POST — Bulk Webhook

```http
POST /webhook/payments/bulk
```

**Request Body:**
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
    "event": "payment.captured",
    "payload": {
      "payment": {
        "entity": {
          "id": "pay_002",
          "status": "captured",
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

### GET — Payment Events

```http
GET /payments/{payment_id}/events
```

**Example:**
```bash
curl -X GET "http://127.0.0.1:8000/payments/pay_001/events" \
-H "accept: application/json"
```

**Response:**
```json
{
  "status": true,
  "message": "Payment events fetched successfully",
  "data": [
    {
      "event_type": "payment.authorized",
      "received_at": "2025-07-07T12:34:25"
    }
  ]
}
```

---

## 🧪 Testing

### Using CURL

```bash
curl -X POST http://127.0.0.1:8000/webhook/payments \
-H "Content-Type: application/json" \
-H "X-Razorpay-Signature: test_secret" \
-d @mock_payloads/payment_authorized.json
```

### Using Python Test Script

```bash
py app/tests/test_webhook.py
```

---

## 📁 Logs

All webhook logs are stored in:

```
logs/webhook_test_logs.json
logs/payment_webhook_service.log
logs/main.log
```

---

## 🔒 Security

- Signature validation using **HMAC SHA256**
- Header: `X-Razorpay-Signature`
- Duplicate event protection via **unique event IDs**

---

## 🔮 Future Improvements

- [ ] Redis Queue Support
- [ ] Celery Background Workers
- [ ] Kafka Integration
- [ ] Retry Mechanism
- [ ] Dead Letter Queue
- [ ] Rate Limiting
- [ ] Webhook Replay System
- [ ] CI/CD Pipeline
- [ ] Unit Testing Coverage

---

## 👨‍💻 Author

**Shivam Kumar**

---
