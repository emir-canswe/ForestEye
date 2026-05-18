import logging
from sqlalchemy.orm import Session
from app.models.db.models import Subscriber, Subscription, GridCell, RiskScore, NotificationSent
from app.notifications.sms import SMSNotifier
from app.notifications.email import EmailNotifier
from app.notifications.push import PushNotifier
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class NotificationDispatcher:
    def __init__(self):
        self.sms = SMSNotifier()
        self.email = EmailNotifier()
        self.push = PushNotifier()

    def _should_send_notification(self, db: Session, sub: Subscription, risk: RiskScore) -> bool:
        """
        Spam önleme kuralları:
        - Aynı hücre için aynı aboneye son 4 saat içinde bildirim gönderilmiş mi?
        - Risk seviyesi abonenin minimum beklentisini karşılıyor mu?
        """
        # Risk seviyesi hiyerarşisi
        levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        sub_level = levels.get(sub.min_risk_level, 3)
        actual_level = levels.get(risk.risk_level, 1)
        
        if actual_level < sub_level:
            return False
            
        # Son 4 saat kontrolü
        four_hours_ago = datetime.utcnow() - timedelta(hours=4)
        recent_notif = db.query(NotificationSent).filter(
            NotificationSent.subscriber_id == sub.subscriber_id,
            NotificationSent.sent_at >= four_hours_ago
        ).join(RiskScore, NotificationSent.risk_score_id == RiskScore.id).filter(
            RiskScore.grid_cell_id == risk.grid_cell_id
        ).first()
        
        if recent_notif:
            return False
            
        return True

    def dispatch_for_risk(self, db: Session, risk: RiskScore, cell: GridCell):
        """
        Risk skoru yüksek/kritik geldiğinde ilgili abonelere bildirim gönderir.
        """
        if risk.risk_level not in ["high", "critical"]:
            return
            
        subscriptions = db.query(Subscription).filter(Subscription.grid_cell_id == risk.grid_cell_id).all()
        
        cell_data = {
            "cell_id": cell.id,
            "il_adi": cell.il_adi,
            "ilce_adi": cell.ilce_adi,
            "risk_score": risk.risk_score,
            "risk_level": risk.risk_level,
            "humidity": risk.humidity,
            "wind_speed": risk.wind_speed,
            "temperature": risk.temperature
        }
        
        for sub in subscriptions:
            subscriber = db.query(Subscriber).filter(Subscriber.id == sub.subscriber_id).first()
            if not subscriber or not subscriber.is_active:
                continue
                
            if not self._should_send_notification(db, sub, risk):
                continue
                
            # E-posta her zaman gönderilsin (varsa)
            if subscriber.email:
                provider_id = self.email.send_alert(subscriber.email, cell_data)
                self._log_notification(db, subscriber.id, risk.id, "email", "sent" if provider_id else "failed", provider_id)
                
            # Kritik durumlarda veya abone istediyse SMS
            if subscriber.phone and risk.risk_level == "critical":
                provider_id = self.sms.send_alert(subscriber.phone, cell_data)
                self._log_notification(db, subscriber.id, risk.id, "sms", "sent" if provider_id else "failed", provider_id)
                
            # Push
            if subscriber.fcm_token:
                provider_id = self.push.send_alert(subscriber.fcm_token, cell_data)
                self._log_notification(db, subscriber.id, risk.id, "push", "sent" if provider_id else "failed", provider_id)

    def _log_notification(self, db: Session, sub_id: int, risk_id: int, channel: str, status: str, provider_id: str):
        log = NotificationSent(
            subscriber_id=sub_id,
            risk_score_id=risk_id,
            channel=channel,
            status=status,
            provider_id=str(provider_id) if provider_id else None
        )
        db.add(log)
        db.commit()
