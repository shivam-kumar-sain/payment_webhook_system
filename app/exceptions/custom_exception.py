class DuplicateWebhookException(Exception):
    def __init__(self,message="Webhook already processed"):
        self.message = message

class InvalidSignatureException(Exception):
    def __init__(self,message="Invalid webhook signature"):
        self.message = message