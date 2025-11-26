
from ..base import ProviderInterface
from ....models.notification_message.email.message import EmailNotificationMessage

class EmailProvider(ProviderInterface[EmailNotificationMessage]): ...