import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailNotifier:
    def __init__(self):
        self.api_key = settings.SENDGRID_API_KEY
        self.from_email = settings.FROM_EMAIL
        
        if self.api_key and "your_key" not in self.api_key:
            self.client = SendGridAPIClient(self.api_key)
        else:
            self.client = None
            logger.warning("SendGrid credentials not configured properly. Emails will not be sent.")

    def send_alert(self, to_email: str, cell_data: dict):
        if not self.client:
            logger.info(f"MOCK Email to {to_email}: Risk level {cell_data.get('risk_score')} for {cell_data.get('il_adi')}")
            return "mock_email_id"

        try:
            subject = f"🔥 YANGIN RİSKİ UYARISI: {cell_data.get('il_adi')} / {cell_data.get('ilce_adi')}"
            
            html_content = f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: auto;">
                <div style="background-color: #DC2626; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
                    <h2 style="margin: 0;">YÜKSEK YANGIN RİSKİ</h2>
                </div>
                <div style="padding: 20px; border: 1px solid #e5e7eb; border-top: none; border-radius: 0 0 8px 8px;">
                    <p><strong>Bölge:</strong> {cell_data.get('il_adi')} / {cell_data.get('ilce_adi')}</p>
                    <p><strong>Risk Skoru:</strong> <span style="font-size: 24px; font-weight: bold; color: #EA580C;">{cell_data.get('risk_score', 0):.0f}/100</span></p>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Sıcaklık:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;">{cell_data.get('temperature', 0):.0f}°C</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Nem:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;">%{cell_data.get('humidity', 0):.0f}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>Rüzgar:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #eee;">{cell_data.get('wind_speed', 0):.1f} m/s</td>
                        </tr>
                    </table>
                    <div style="margin-top: 25px; text-align: center;">
                        <a href="https://yangin-uyari.gov.tr/harita/{cell_data.get('cell_id')}" 
                           style="background-color: #1F2937; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                           Haritada Görüntüle
                        </a>
                    </div>
                </div>
            </div>
            """

            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )

            response = self.client.send(message)
            return response.headers.get('X-Message-Id', 'sent')
        except Exception as e:
            logger.error(f"Failed to send Email to {to_email}: {e}")
            return None
