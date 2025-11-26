from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from ...models.notification_message.message_base import BaseNotificationMessage

M = TypeVar("M", bound=BaseNotificationMessage)

class ProviderInterface(ABC, Generic[M]):

    @abstractmethod
    async def send(self, message: M) -> None: ... 