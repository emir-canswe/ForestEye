import logging
import firebase_admin
from firebase_admin import credentials, messaging
from app.core.config import settings
import os

logger = logging.getLogger(__name__)

class PushNotifier:
    def __init__(self):
        self.cert_path = settings.FIREBASE_CREDENTIALS_PATH
        
        if self.cert_path and os.path.exists(self.cert_path):
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.cert_path)
                firebase_admin.initialize_app(cred)
            self.is_ready = True
        else:
            self.is_ready = False
            logger.warning("Firebase credentials not found. Push notifications will not be sent.")

    def send_alert(self, fcm_token: str, cell_data: dict):
        if not self.is_ready:
            logger.info(f"MOCK Push to {fcm_token}: Risk level {cell_data.get('risk_score')} for {cell_data.get('il_adi')}")
            return "mock_push_id"

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=f"🔥 Yangın Riski: {cell_data.get('il_adi')}",
                    body=f"Risk skoru: {cell_data.get('risk_score', 0):.0f}/100 — Nem %{cell_data.get('humidity', 0):.0f}",
                ),
                data={
                    "cell_id": str(cell_data.get("cell_id")),
                    "risk_score": str(cell_data.get("risk_score")),
                    "risk_level": str(cell_data.get("risk_level")),
                },
                token=fcm_token,
            )
            response = messaging.send(message)
            return response
        except Exception as e:
            logger.error(f"Failed to send Push Notification to {fcm_token}: {e}")
            return None
