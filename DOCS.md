# DOCS.md

# Payment Webhook System Documentation

## Overview

This project is a production-ready webhook processing system built using FastAPI and PostgreSQL.

The system receives payment webhooks, validates signatures, prevents duplicate event processing, stores webhook events, and provides APIs to fetch payment event history.

---

# Architecture

```text
Client/Webhook Provider
            ↓
        API Router
            ↓
      Service Layer
            ↓
    Repository Layer
            ↓
        PostgreSQL
```

---

# Core Features

## 1. Webhook Signature Validation

The application validates webhook signatures using HMAC SHA256.

Header used:

```http
X-Razorpay-Signature
```

Validation flow:

```text
Raw Request Body
        ↓
Generate HMAC SHA256
        ↓
Compare With Header Signature
        ↓
Valid / Invalid
```

---

# 2. Idempotency Protection

Duplicate webhook events are prevented using unique event IDs.

If the same event is received multiple times:

* Existing event is detected
* Duplicate processing is skipped
* Exception is raised

Example:

```json
{
  "status": false,
  "message": "Duplicate webhook event"
}
```

---

# 3. Bulk Webhook Processing

The system supports:

* Single webhook payload
* Multiple webhook payloads

Accepted formats:

## Single Payload

```json
{
  "event": "payment.authorized",
  "id": "evt_auth_001"
}
```

## Bulk Payload

```json
[
  {
    "event": "payment.authorized",
    "id": "evt_auth_001"
  },
  {
    "event": "payment.authorized",
    "id": "evt_auth_002"
  }
]
```

---

# Project Layers

## Router Layer

Responsible for:

* Request handling
* Dependency injection
* Route management
* API response handling

Location:

```text
app/api/
```

---

# Service Layer

Responsible for:

* Business logic
* Webhook processing
* Signature verification orchestration
* Bulk processing
* Logging

Location:

```text
app/services/
```

---

# Repository Layer

Responsible for:

* Database operations
* Query handling
* CRUD operations

Location:

```text
app/repositories/
```

---

# Schema Layer

Responsible for:

* Request validation
* Response validation
* Nested payload parsing

Location:

```text
app/schemas/
```

---

# Utility Layer

Responsible for:

* Signature helpers
* Payload parsers
* Common reusable functions

Location:

```text
app/utils/
```

---

# Exception Layer

Responsible for:

* Custom exceptions
* Global exception handling
* Standardized error responses

Location:

```text
app/exceptions/
```

---

# Database Design

## payment_events Table

| Column     | Type     | Description              |
| ---------- | -------- | ------------------------ |
| _id        | Integer  | Primary key              |
| event_id   | String   | Unique webhook event ID  |
| payment_id | String   | Payment identifier       |
| event_type | String   | Webhook event type       |
| payload    | JSON     | Complete webhook payload |
| created_at | DateTime | Record creation time     |
| updated_at | DateTime | Record update time       |

---

# API Documentation

# 1. Process Webhook

## Endpoint

```http
POST /webhook/payments
```

## Headers

```http
Content-Type: application/json
X-Razorpay-Signature: TEST_SIGNATURE
```

---

# Single Webhook Example

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

# Bulk Webhook Example

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

# 2. Get Payment Events

## Endpoint

```http
GET /payments/{payment_id}/events
```

## Example

```bash
curl -X GET \
"http://127.0.0.1:8000/payments/pay_020/events" \
-H "accept: application/json"
```

## Response

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

# Logging System

Logs include:

* Request logs
* Response logs
* Error logs
* Duplicate webhook logs
* Bulk processing logs

Log location:

```text
logs/webhook_test_logs.json
```

---

# Testing

## CURL Test

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

# Security Considerations

* HMAC SHA256 verification
* Duplicate webhook prevention
* Structured exception handling
* Security headers middleware
* Input schema validation

---

# Future Improvements

* Redis Queue
* Celery Workers
* Kafka Integration
* Retry Mechanism
* Docker Support
* Kubernetes Deployment
* CI/CD Pipeline
* Unit Testing
* Integration Testing
* Metrics Monitoring

---

# Author

Shivam Kumar
