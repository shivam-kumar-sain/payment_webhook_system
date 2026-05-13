from fastapi import Request
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logger import get_logger
from app.utils.signature_helper import (verify_signature)
from app.utils.payload_parser import (parse_payment_payload)
from app.schemas.request.webhook_request_schema import (WebhookRequestSchema)
from app.repositories.payment_event_repository import (PaymentEventRepository)
from app.exceptions.custom_exception import (DuplicateWebhookException,InvalidSignatureException)


class PaymentWebhookService:

    def __init__(self, db: Session):

        self.logger = get_logger(__name__)
        self.logger.setLevel(settings.log_level)
        self.db = db
        self.repo = PaymentEventRepository(db)

    def _process_single_webhook(self,payload: WebhookRequestSchema):
        event_id = payload.id
        self.logger.info(f"Checking duplicate webhook event_id={event_id}")
        existing_event = self.repo.get_by_event_id(event_id)
        if existing_event:

            self.logger.warning(f"Duplicate webhook received event_id={event_id}")
            raise DuplicateWebhookException()

        self.logger.info(f"Parsing webhook payload event_id={event_id}")
        event_data = parse_payment_payload(payload)

        self.logger.info(f"Saving webhook event event_id={event_id}")
        created_event = self.repo.create( event_data)

        self.logger.info(f"Webhook processed successfully event_id={event_id}")

        return {
            "event_id": created_event.event_id,
            "payment_id": created_event.payment_id,
            "event_type": created_event.event_type,
            "status": "processed"
        }
    

    """
        --------------------------------------------------
        Process Single Webhooks
        --------------------------------------------------
    """
    async def process_webhook(self,request: Request,payload: WebhookRequestSchema):
        try:
            self.logger.info("Webhook request received")
            raw_body = await request.body()
            signature = request.headers.get("X-Razorpay-Signature")
            if not signature:
                self.logger.warning("Missing webhook signature")
                raise InvalidSignatureException()

            self.logger.info("Verifying webhook signature")
            verify_signature(raw_body,signature)
            self.logger.info("Webhook signature verified")

            result = self._process_single_webhook(payload)
            return {
                "status": True,
                "message": "Webhook processed successfully",
                "data": result
            }

        except DuplicateWebhookException:
            raise

        except InvalidSignatureException:
            raise

        except Exception as e:
            self.logger.exception(f"Webhook processing failed: {str(e)}")
            raise

    """
        --------------------------------------------------
        Process Bulk Webhooks
        --------------------------------------------------
    """
    def process_bulk_webhooks(self,payloads: list):
        success = []
        issues = []
        for payload in payloads:
            try:
                validated_payload = (WebhookRequestSchema(**payload))
                result = (self._process_single_webhook(validated_payload))
                success.append(result)

            except DuplicateWebhookException:
                self.logger.warning(f"Duplicate skipped event_id={payload.get('id')}")
                issues.append({"event_id": payload.get("id"),"status": "duplicate"})
            except Exception as e:
                self.logger.exception(f"Bulk webhook failed: {str(e)}")
                issues.append({
                    "event_id": payload.get("id"),
                    "status": "failed",
                    "error": str(e)
                })

        self.logger.info(
            f"Bulk webhook processing completed "
            f"success={len(success)} "
            f"issues={len(issues)}"
        )

        return {
            "status": True,
            "message": "Bulk webhook processed successfully",
            "success": success,
            "issues": issues
        }

    # async def process_webhook(self,request: Request,payload: WebhookRequestSchema):
    #     try:
    #         self.logger.info("Webhook request received")
    #         raw_body = await request.body()
    #         signature = request.headers.get("X-Razorpay-Signature")

    #         if not signature:

    #             self.logger.warning("Missing webhook signature")

    #             raise InvalidSignatureException()

    #         self.logger.info("Verifying webhook signature")

    #         verify_signature(raw_body,signature)
    #         self.logger.info("Webhook signature verified")
    #         event_id = payload.id
    #         self.logger.info(f"Checking duplicate webhook for event_id={event_id}")
    #         existing_event = self.repo.get_by_event_id(event_id)
    #         if existing_event:

    #             self.logger.warning(f"Duplicate webhook received event_id={event_id}")
    #             raise DuplicateWebhookException()

    #         self.logger.info(f"Parsing webhook payload event_id={event_id}")
    #         event_data = parse_payment_payload(payload)

    #         self.logger.info(f"Saving webhook event event_id={event_id}")

    #         created_event = self.repo.create(event_data)
    #         self.logger.info(f"Webhook processed successfully event_id={event_id}")

    #         return {
    #             "status": True,
    #             "message": "Webhook processed successfully",
    #             "data": {
    #                 "event_id": created_event.event_id,
    #                 "payment_id": created_event.payment_id,
    #                 "event_type": created_event.event_type
    #             }
    #         }

    #     except DuplicateWebhookException:
    #         raise

    #     except InvalidSignatureException:
    #         raise

    #     except Exception as e:
    #         self.logger.error(f"Webhook processing failed: {str(e)}")
    #         raise

    """
        --------------------------------------------------
        Process Bulk Webhooks
        --------------------------------------------------
    """

    # def process_bulk_webhooks(self,payloads: list):
    #     results = []
    #     for payload in payloads:
    #         try:
    #             validated_payload = (WebhookRequestSchema(**payload))
    #             result = (self.process_webhook(validated_payload))
    #             results.append(result)

    #         except DuplicateWebhookException:
    #             self.logger.warning(f"Duplicate skipped event_id={payload.get('id')}")
    #             results.append({
    #                 "event_id": payload.get("id"),
    #                 "status": "duplicate"
    #             })

    #         except Exception as e:
    #             self.logger.exception(f"Bulk webhook failed: {str(e)}")
    #             results.append({
    #                 "event_id": payload.get("id"),
    #                 "status": "failed",
    #                 "error": str(e)
    #             })

    #     self.logger.info(f"Bulk webhook processing completed count={len(results)}")
    #     return {
    #         "status": True,
    #         "message": "Bulk webhook processed successfully",
    #         "data": results
    #     }


    def get_payment_events(self,payment_id: str):
        try:
            self.logger.info(f"Fetching payment events payment_id={payment_id}")
            events = self.repo.get_payment_events(payment_id)
            self.logger.info(f"Fetched {len(events)} events for payment_id={payment_id}")
            return [
                {
                    "event_type": event.event_type,
                    "received_at": event.received_at
                }
                for event in events
            ]

        except Exception as e:
            self.logger.error(f"Failed to fetch payment events: {str(e)}")

            raise