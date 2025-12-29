import logging
from celery import shared_task
from login.email_service import EmailNotificationService

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 60})
def send_login_alert_email(self, username, staff_code, login_datetime):
    """
    Async task to send login alert email.
    Runs in background - doesn't block login response.
    """
    try:
        logger.info(f"📧 [BACKGROUND] Sending login alert for {username}...")
        
        email_service = EmailNotificationService()
        result = email_service.send_login_alert(
            username=username,
            staff_code=staff_code,
            login_datetime=login_datetime
        )
        
        if result.get("success"):
            logger.info(f"✅ [BACKGROUND] Login alert sent for {username}")
            return {"status": "success", "user": username}
        else:
            logger.error(f"❌ [BACKGROUND] Email failed: {result.get('error')}")
            raise Exception(result.get('error'))
            
    except Exception as e:
        logger.error(f"❌ [BACKGROUND] Error in send_login_alert_email: {str(e)}")
        raise  # Triggers retry