
from ..base import ProviderInterface
from ....models.notification_message.sms.message import SMSNotificationMessage

class SMSProvider(ProviderInterface[SMSNotificationMessage]): ...