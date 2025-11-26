from typing import Sequence, Generic, TypeVar
from abc import ABC, abstractmethod

from ..providers.base import ProviderInterface
from ...models.notification_message.message_base import BaseNotificationMessage
from ...utils.log import Log

M = TypeVar("M", bound=BaseNotificationMessage)
P = TypeVar("P", bound=ProviderInterface[M])

class HandlerInterface(ABC, Generic[P, M]):
    """
    Base class for all message handlers.
    Includes fallback provider logic.
    """

    def __init__(self, providers: Sequence[P]):
        if not providers:
            raise ValueError(f"{self.__class__.__name__} requires at least one provider")
        self._providers = list(providers)

    @property
    def providers(self) -> list[P]:
        return self._providers

    @abstractmethod
    async def handle(self, message: M) -> None:
        """Concrete handler must implement this and call self._send_via_providers()"""
        ...

    async def _send_via_providers(self, message: M) -> None:
        """
        Generic fallback logic.
        Tries providers one by one until one succeeds.
        """

        last_error = None

        for provider in self.providers:
            try:
                await provider.send(message)
                Log.success(
                    f"[{self.__class__.__name__}] "
                    f"{provider.__class__.__name__} succeeded"
                )
                return
            except Exception as e:
                Log.error(
                    f"[{self.__class__.__name__}] "
                    f"Provider {provider.__class__.__name__} failed: {e}"
                )
                last_error = e

        raise RuntimeError(
            f"[{self.__class__.__name__}] All providers failed"
        ) from last_error
