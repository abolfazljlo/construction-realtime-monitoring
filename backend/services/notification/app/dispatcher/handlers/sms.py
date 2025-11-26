from .base import HandlerInterface
from ..providers.sms.base import SMSProvider
from ...models.notification_message.sms.message import SMSNotificationMessage

class SMSHandler(HandlerInterface[SMSProvider, SMSNotificationMessage]):

    async def handle(self, message):
        return await self._send_via_providers(message)