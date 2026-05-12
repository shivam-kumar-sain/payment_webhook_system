payment_webhook_system/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   ├── public/
│   │   │   └── webhook_routes.py
│   │   │
│   │   ├── private/
│   │   │   └── payment_routes.py
│   │   │
│   │   └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logger.py
│   │   └── constants.py
│   │
│   ├── models/
│   │   └── payment_event_model.py
│   │
│   ├── repositories/
│   │   └── payment_event_repository.py
│   │
│   ├── services/
│   │   └── payment_webhook_service.py
│   │
│   ├── schemas/
│   │   ├── request/
│   │   │   └── webhook_request_schema.py
│   │   │
│   │   └── response/
│   │       └── payment_response_schema.py
│   │
│   ├── middleware/
│   │   └── request_logging.py
│   │
│   ├── exceptions/
│   │   ├── custom_exception.py
│   │   └── handlers.py
│   │
│   ├── dependencies/
│   │   └── auth_dependency.py
│   │
│   ├── utils/
│   │   ├── signature_helper.py
│   │   ├── payload_parser.py
│   │   └── datetime_helper.py
│   │
│   └── tests/
│       ├── test_webhook.py
│       └── test_payment_events.py
│
├── mock_payloads/
│   ├── payment_authorized.json
│   ├── payment_captured.json
│   └── payment_failed.json
│
├── alembic/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── DOCS.md
└── docker-compose.yml