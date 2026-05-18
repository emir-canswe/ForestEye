import logging
from twilio.rest import Client
from app.core.config import settings

logger = logging.getLogger(__name__)

class SMSNotifier:
    def __init__(self):
        self.sid = settings.TWILIO_ACCOUNT_SID
        self.token = settings.TWILIO_AUTH_TOKEN
        self.from_phone = settings.TWILIO_PHONE_NUMBER
        
        # Don't initialize client if credentials are missing/dummy
        if self.sid and "your_sid" not in self.sid:
            self.client = Client(self.sid, self.token)
        else:
            self.client = None
            logger.warning("Twilio credentials not configured properly. SMS will not be sent.")

    def send_alert(self, to_phone: str, cell_data: dict):
        if not self.client:
            logger.info(f"MOCK SMS to {to_phone}: Risk level {cell_data.get('risk_score')} for {cell_data.get('il_adi')}")
            return "mock_message_id"

        try:
            message = (
                f"⚠️ YANGIN RİSKİ UYARISI\n"
                f"Bölge: {cell_data.get('il_adi')} / {cell_data.get('ilce_adi')}\n"
                f"Risk Skoru: {cell_data.get('risk_score', 0):.0f}/100\n"
                f"Nem: %{cell_data.get('humidity', 0):.0f} | "
                f"Rüzgar: {cell_data.get('wind_speed', 0):.1f} m/s | "
                f"Sıcaklık: {cell_data.get('temperature', 0):.0f}°C\n"
                f"Detay: https://yangin-uyari.gov.tr/harita/{cell_data.get('cell_id')}"
            )

            msg = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone
            )
            return msg.sid
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_phone}: {e}")
            return None
