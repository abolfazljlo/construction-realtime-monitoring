from .base import HandlerInterface
from ..providers.email.base import EmailProvider
from ...models.notification_message.email.message import EmailNotificationMessage

class EmailHandler(HandlerInterface[EmailProvider, EmailNotificationMessage]):

    async def handle(self, message):
        return await self._send_via_providers(message)