from django.conf import settings
from pywebpush import webpush, WebPushException
import logging
import json

logger = logging.getLogger(__name__)

# Hardcoded VAPID keys for simplicity for now, or fetch from env.
# In production, these should be env variables.
# Generate with: openssl ecparam -name prime256v1 -genkey -noout -out private_key.pem
#                openssl ec -in private_key.pem -pubout -out public_key.pem
# Or using pywebpush CLI. 
# For this demo, I'll assume we can pass them or use a library to generate if missing, 
# but usually it's best to have stable keys.

def send_web_push(subscription_info, message_body):
    """
    subscription_info: dict containing 'endpoint', 'keys' {'p256dh', 'auth'}
    message_body: str or json
    """
    private_key = settings.VAPID_PRIVATE_KEY
    if not private_key:
        logger.warning("No VAPID_PRIVATE_KEY configured.")
        return

    try:
        webpush(
            subscription_info=subscription_info,
            data=message_body,
            vapid_private_key=private_key,
            vapid_claims={
                "sub": "mailto:admin@surchaing.com"
            }
        )
        logger.info(f"Web push sent to {subscription_info.get('endpoint')[:20]}...")
    except WebPushException as e:
        logger.error(f"Web Push failed: {repr(e)}")
        # If 410 Gone, we should delete the subscription
        if e.response and e.response.status_code == 410:
            return "DELETE"
